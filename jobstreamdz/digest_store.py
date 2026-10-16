from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from urllib.parse import urlsplit

from .sheets import extract_apply_url


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_text(value: str) -> str:
    return " ".join(_to_text(value).split())


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _to_utc_iso(value: datetime) -> str:
    normalized = value.astimezone(timezone.utc).replace(microsecond=0)
    return normalized.isoformat().replace("+00:00", "Z")


def _telegram_result(payload: dict[str, Any]) -> dict[str, Any]:
    result = payload.get("result", {})
    if isinstance(result, dict):
        return result
    return {}


def _published_at(telegram_response: dict[str, Any]) -> datetime:
    result = _telegram_result(telegram_response)
    epoch_raw = result.get("date")

    try:
        epoch = int(epoch_raw)
        return datetime.fromtimestamp(epoch, tz=timezone.utc)
    except (TypeError, ValueError, OSError, OverflowError):
        return _utc_now()


def _digest_id(published_at: datetime, telegram_response: dict[str, Any]) -> str:
    result = _telegram_result(telegram_response)
    message_id = _to_text(result.get("message_id", ""))
    suffix = "".join(
        char for char in message_id if char.isalnum() or char in {"-", "_"}
    )

    if not suffix:
        suffix = str(int(published_at.timestamp()))

    timestamp = published_at.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"digest_{timestamp}_{suffix}"


def _source_from_domain(url: str) -> str:
    host = urlsplit(url).netloc.lower()
    if not host:
        return "unknown"

    if "linkedin.com" in host:
        return "LinkedIn"
    if "emploitic.com" in host:
        return "Emploitic"
    if "naukrigulf.com" in host:
        return "NaukriGulf"
    if "jobindz" in host:
        return "Jobindz"
    if "jobdz" in host:
        return "Jobdz"

    return "unknown"


def _safe_source(job: dict[str, str], apply_url: str) -> str:
    source_raw = _normalize_text(job.get("source", ""))
    if source_raw:
        normalized = source_raw.lower()
        if normalized == "linkedin":
            return "LinkedIn"
        if normalized == "naukrigulf":
            return "NaukriGulf"
        if normalized == "emploitic":
            return "Emploitic"
        if normalized == "jobdz":
            return "Jobdz"
        if normalized == "jobindz":
            return "Jobindz"
        return source_raw

    inferred = _source_from_domain(apply_url)
    return inferred


def _job_payload(job: dict[str, str], fingerprint: str) -> dict[str, str]:
    apply_url = extract_apply_url(job)
    source = _safe_source(job, apply_url)

    return {
        "id": fingerprint,
        "fingerprint": fingerprint,
        "source": source,
        "title": _normalize_text(job.get("title", "")) or "Not specified",
        "company_name": _normalize_text(job.get("company_name", "")) or "Not specified",
        "location": _normalize_text(job.get("location", "")) or "Not specified",
        "apply_url": apply_url,
        "published_date": _normalize_text(job.get("published_date", ""))
        or "Not specified",
        "published_time_utc": _normalize_text(job.get("published_time_utc", ""))
        or "Not specified",
        "job_id": _normalize_text(job.get("job_id", "")) or "Not specified",
        "job_alias": _normalize_text(job.get("job_alias", "")) or "Not specified",
        "contract_type": _normalize_text(job.get("contract_type", "")),
        "experience_years": _normalize_text(job.get("experience_years", "")),
        "job_level": _normalize_text(job.get("job_level", "")),
        "work_mode": _normalize_text(job.get("work_mode", "")),
    }


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None

    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=str(path.parent),
            delete=False,
        ) as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
            temp_path = Path(handle.name)

        temp_path.replace(path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink(missing_ok=True)


def persist_published_digest(
    *,
    digests_dir: Path,
    latest_snapshot_file: Path,
    feed_name: str,
    jobs: list[dict[str, str]],
    fingerprints: list[str],
    telegram_response: dict[str, Any],
    chat_id: str,
    channel_label: str,
) -> str:
    if len(jobs) != len(fingerprints):
        raise ValueError(
            "jobs and fingerprints must have matching lengths "
            f"(got {len(jobs)} and {len(fingerprints)})"
        )

    published_at = _published_at(telegram_response)
    digest_id = _digest_id(published_at, telegram_response)
    published_at_iso = _to_utc_iso(published_at)
    result = _telegram_result(telegram_response)

    payload = {
        "digest_id": digest_id,
        "feed": _to_text(feed_name) or "main",
        "published_at": published_at_iso,
        "job_count": len(jobs),
        "channel": {
            "chat_id": _to_text(chat_id),
            "label": _to_text(channel_label) or "JobStream DZ",
        },
        "telegram": {
            "ok": bool(telegram_response.get("ok")),
            "message_id": result.get("message_id"),
            "date": result.get("date"),
        },
        "jobs": [
            _job_payload(job=job, fingerprint=fingerprint)
            for fingerprint, job in zip(fingerprints, jobs)
        ],
    }

    immutable_path = digests_dir / f"{digest_id}.json"
    _atomic_write_json(immutable_path, payload)
    _atomic_write_json(latest_snapshot_file, payload)

    return digest_id
