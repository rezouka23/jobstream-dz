from __future__ import annotations

import math
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import Settings
from .digest_store import persist_published_digest
from .sheets import (
    build_sheets_service,
    fetch_sheet_rows,
    fingerprint_job,
    has_usable_apply_url,
)
from .state import PostedState, load_state, save_state
from .telegram_client import build_digest_message, send_telegram_message

LOGGER = logging.getLogger("jobstreamdz.publisher")


@dataclass(frozen=True)
class FeedSpec:
    name: str
    sheet_name: str
    poll_seconds: int
    post_limit: int
    require_full_batch: bool
    digests_dir: Path
    latest_digest_file: Path


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def _collect_unseen_jobs(
    rows: list[dict[str, str]],
    state: PostedState,
) -> tuple[list[tuple[str, dict[str, str]]], int]:
    unseen: list[tuple[str, dict[str, str]]] = []
    cycle_seen: set[str] = set()
    skipped_without_links = 0

    for row in rows:
        if not has_usable_apply_url(row):
            skipped_without_links += 1
            continue

        fingerprint = fingerprint_job(row)
        if fingerprint in state.fingerprints:
            continue
        if fingerprint in cycle_seen:
            continue
        unseen.append((fingerprint, row))
        cycle_seen.add(fingerprint)

    return unseen, skipped_without_links


def _build_feed_specs(settings: Settings) -> list[FeedSpec]:
    feeds = [
        FeedSpec(
            name="main",
            sheet_name=settings.sheet_name,
            poll_seconds=settings.poll_seconds,
            post_limit=settings.post_limit,
            require_full_batch=settings.require_full_batch,
            digests_dir=settings.digests_dir,
            latest_digest_file=settings.latest_digest_file,
        )
    ]

    if settings.remote_enabled:
        feeds.append(
            FeedSpec(
                name="remote",
                sheet_name=settings.remote_sheet_name,
                poll_seconds=settings.remote_poll_seconds,
                post_limit=settings.remote_post_limit,
                require_full_batch=settings.remote_require_full_batch,
                digests_dir=settings.remote_digests_dir,
                latest_digest_file=settings.remote_latest_digest_file,
            )
        )

    return feeds


def process_cycle(
    settings: Settings,
    service: Any,
    state: PostedState,
    feed: FeedSpec,
) -> int:
    rows = fetch_sheet_rows(
        service=service,
        spreadsheet_id=settings.spreadsheet_id,
        sheet_name=feed.sheet_name,
        max_rows=settings.max_rows,
    )
    if not rows:
        LOGGER.info("[%s] No rows found in sheet tab '%s'.", feed.name, feed.sheet_name)
        return 0

    unseen, skipped_without_links = _collect_unseen_jobs(rows, state)
    unseen_count = len(unseen)

    if skipped_without_links:
        LOGGER.info(
            "[%s] Skipped %s rows without usable apply URLs.",
            feed.name,
            skipped_without_links,
        )

    if unseen_count == 0:
        LOGGER.info("[%s] No unseen jobs with usable apply URLs this cycle.", feed.name)
        return 0

    if feed.require_full_batch and unseen_count < feed.post_limit:
        LOGGER.info(
            "[%s] Unseen jobs available: %s, waiting for at least %s before posting.",
            feed.name,
            unseen_count,
            feed.post_limit,
        )
        return 0

    batch = unseen[: feed.post_limit]
    jobs = [row for _, row in batch]
    message = build_digest_message(
        jobs=jobs,
        channel_label=settings.telegram_channel_label,
        feed_name=feed.name,
    )

    telegram_response = send_telegram_message(
        bot_token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
        text=message,
    )
    if not telegram_response.get("ok"):
        raise RuntimeError("Telegram send did not return ok=true")

    fingerprints = [fingerprint for fingerprint, _ in batch]
    digest_id = persist_published_digest(
        digests_dir=feed.digests_dir,
        latest_snapshot_file=feed.latest_digest_file,
        feed_name=feed.name,
        jobs=jobs,
        fingerprints=fingerprints,
        telegram_response=telegram_response,
        chat_id=settings.telegram_chat_id,
        channel_label=settings.telegram_channel_label,
    )

    for fingerprint in fingerprints:
        state.fingerprints.add(fingerprint)
    save_state(settings.state_file, state)

    LOGGER.info(
        "[%s] Published digest with %s jobs (digest_id=%s).",
        feed.name,
        len(batch),
        digest_id,
    )
    return len(batch)


def _next_sleep_seconds(feeds: list[FeedSpec], last_attempts: dict[str, float]) -> int:
    now = time.time()
    waits: list[int] = []

    for feed in feeds:
        last_attempt = last_attempts.get(feed.name)
        if last_attempt is None:
            waits.append(1)
            continue

        remaining = math.ceil(feed.poll_seconds - (now - last_attempt))
        waits.append(max(1, remaining))

    return min(waits) if waits else 1


def run(settings: Settings) -> None:
    _setup_logging()
    feeds = _build_feed_specs(settings)

    LOGGER.info("Starting JobStream DZ Telegram publisher with %s feed(s).", len(feeds))
    for feed in feeds:
        LOGGER.info(
            "Feed '%s': tab='%s', poll=%ss, digest_size=%s, full_batch=%s",
            feed.name,
            feed.sheet_name,
            feed.poll_seconds,
            feed.post_limit,
            feed.require_full_batch,
        )

    state = load_state(settings.state_file)
    LOGGER.info("Loaded %s known fingerprints.", len(state.fingerprints))

    service = build_sheets_service(
        service_account_file=str(settings.google_service_account_file)
        if settings.google_service_account_file
        else None,
        service_account_json=settings.google_service_account_json,
    )

    if settings.single_run:
        for feed in feeds:
            try:
                process_cycle(settings, service, state, feed)
            except Exception:
                LOGGER.exception("[%s] Cycle failed.", feed.name)
        LOGGER.info("SINGLE_RUN=true, exiting after one pass across feeds.")
        return

    last_attempts: dict[str, float] = {}

    while True:
        for feed in feeds:
            last_attempt = last_attempts.get(feed.name)
            now = time.time()
            if last_attempt is not None and now - last_attempt < feed.poll_seconds:
                continue

            try:
                process_cycle(settings, service, state, feed)
            except Exception:
                LOGGER.exception("[%s] Cycle failed.", feed.name)
            finally:
                last_attempts[feed.name] = time.time()

        sleep_seconds = _next_sleep_seconds(feeds, last_attempts)
        LOGGER.info("Sleeping %s seconds.", sleep_seconds)
        time.sleep(sleep_seconds)
