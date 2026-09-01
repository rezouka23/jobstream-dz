"""Single-run orchestration and resilient loop scheduler."""

from __future__ import annotations

import argparse
import logging
import time
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from .config import ScraperConfig
from .http import build_session
from .schema import Job
from .sheets import GoogleSheetsWriter, build_sheets_service
from .sources import (
    EmploiticAdapter,
    JobindzAdapter,
    LinkedInAdapter,
    NaukriGulfAdapter,
    OuedknissAdapter,
)
from .sources.base import SourceAdapter
from .state import JsonDedupState

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RunResult:
    fetched: int
    inserted: int
    duplicates: int
    source_errors: int


def build_adapters(config: ScraperConfig) -> list[SourceAdapter]:
    session = build_session()
    common = {"timeout": config.request_timeout, "delay": config.request_delay}
    available: dict[str, SourceAdapter] = {
        "emploitic": EmploiticAdapter(session, **common),
        "naukrigulf": NaukriGulfAdapter(session, **common),
        "jobindz": JobindzAdapter(session, **common),
        "ouedkniss": OuedknissAdapter(session, **common),
        "linkedin": LinkedInAdapter(
            config.linkedin_search_terms,
            hours_old=config.linkedin_hours_old,
            results_wanted=config.linkedin_results_wanted,
            remote_only=config.linkedin_remote_only,
            delay=config.request_delay,
        ),
    }
    unknown = sorted(set(config.sources) - available.keys())
    if unknown:
        raise ValueError(f"Unknown scraper source(s): {', '.join(unknown)}")
    return [available[name] for name in config.sources]


def run_once(
    config: ScraperConfig | None = None,
    *,
    adapters: Iterable[SourceAdapter] | None = None,
    writer: GoogleSheetsWriter | None = None,
    state: JsonDedupState | None = None,
) -> RunResult:
    config = config or ScraperConfig.from_env()
    state = state or JsonDedupState(config.state_file)
    writer = writer or GoogleSheetsWriter(
        build_sheets_service(), config.require_spreadsheet_id(), config.sheet_name
    )

    fetched_jobs: list[Job] = []
    source_errors = 0
    for adapter in build_adapters(config) if adapters is None else adapters:
        try:
            source_jobs = adapter.fetch()
        except Exception:
            source_errors += 1
            LOGGER.exception("Source %s failed", adapter.name)
            continue
        LOGGER.info("Source %s fetched %d jobs", adapter.name, len(source_jobs))
        fetched_jobs.extend(source_jobs)

    seen = state.load()
    cycle_seen: set[str] = set()
    new_jobs: list[Job] = []
    for job in fetched_jobs:
        if job.provider_job_id in seen or job.provider_job_id in cycle_seen:
            continue
        cycle_seen.add(job.provider_job_id)
        new_jobs.append(job)
    new_jobs.sort(
        key=lambda item: (item.published_date, item.published_time_utc), reverse=True
    )

    inserted = writer.write(new_jobs)
    if inserted != len(new_jobs):
        raise RuntimeError(f"Sheets writer reported {inserted} of {len(new_jobs)} rows written")
    state.add(job.provider_job_id for job in new_jobs)
    duplicates = len(fetched_jobs) - len(new_jobs)
    LOGGER.info(
        "Scrape complete: fetched=%d inserted=%d duplicates=%d sources=%s",
        len(fetched_jobs), inserted, duplicates,
        dict(Counter(job.source for job in new_jobs)),
    )
    return RunResult(len(fetched_jobs), inserted, duplicates, source_errors)


def run_loop(config: ScraperConfig | None = None) -> None:
    config = config or ScraperConfig.from_env()
    LOGGER.info("Scraper loop active every %d seconds", config.interval_seconds)
    while True:
        try:
            run_once(config)
        except Exception:
            LOGGER.exception("Scrape cycle failed")
        time.sleep(config.interval_seconds)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Aggregate Algerian jobs into Google Sheets")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="run one scrape cycle (default)")
    mode.add_argument("--loop", action="store_true", help="run continuously")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    config = ScraperConfig.from_env()
    if args.loop:
        run_loop(config)
    else:
        run_once(config)
    return 0
