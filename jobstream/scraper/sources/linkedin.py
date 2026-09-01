"""Optional LinkedIn adapter powered by python-jobspy."""

from __future__ import annotations

import logging
import re
import time
from collections.abc import Callable
from typing import Any

from ..schema import Job
from ..text import clean_text, stable_fallback_id, utc_parts

LOGGER = logging.getLogger(__name__)


class LinkedInAdapter:
    name = "linkedin"

    def __init__(
        self,
        search_terms: tuple[str, ...],
        *,
        hours_old: int = 168,
        results_wanted: int = 50,
        remote_only: bool = False,
        delay: float = 0.2,
        scraper: Callable[..., Any] | None = None,
    ):
        self.search_terms = search_terms
        self.hours_old = hours_old
        self.results_wanted = results_wanted
        self.remote_only = remote_only
        self.delay = delay
        self._scraper = scraper

    def fetch(self) -> list[Job]:
        scrape_jobs = self._scraper or self._load_jobspy()
        jobs: list[Job] = []
        for term in self.search_terms:
            try:
                frame = scrape_jobs(
                    site_name=["linkedin"],
                    search_term=term,
                    location="Algeria",
                    results_wanted=self.results_wanted,
                    hours_old=self.hours_old,
                    linkedin_fetch_description=True,
                    **({"is_remote": True} if self.remote_only else {}),
                )
                jobs.extend(self.normalize(row) for row in self._records(frame))
            except Exception:
                LOGGER.exception("LinkedIn search failed for term %r", term)
            if self.delay:
                time.sleep(self.delay)
        return jobs

    @staticmethod
    def _load_jobspy() -> Callable[..., Any]:
        try:
            from jobspy import scrape_jobs
        except ImportError as exc:
            raise RuntimeError(
                "LinkedIn is enabled but python-jobspy is not installed; "
                "install the optional scraper dependency"
            ) from exc
        return scrape_jobs

    @staticmethod
    def _records(frame: Any) -> list[dict[str, Any]]:
        if frame is None:
            return []
        if hasattr(frame, "to_dict"):
            return list(frame.to_dict(orient="records"))
        return list(frame)

    @classmethod
    def normalize(cls, raw: dict[str, Any]) -> Job:
        url = clean_text(raw.get("job_url") or raw.get("url"))
        match = re.search(r"(?:/jobs/view/|[?&](?:currentJobId|jobId)=)(\d+)", url)
        job_id = match.group(1) if match else stable_fallback_id(
            cls.name,
            (url, raw.get("title"), raw.get("company"), raw.get("location")),
        )
        published_date, published_time = utc_parts(raw.get("date_posted"))
        return Job.create(
            source=cls.name,
            job_id=job_id,
            title=raw.get("title"),
            company_name=raw.get("company"),
            location=raw.get("location"),
            profession=raw.get("title"),
            contract_type=raw.get("job_type"),
            work_mode="Remote" if raw.get("is_remote") is True else "",
            published_date=published_date,
            published_time_utc=published_time,
            job_alias=url.rstrip("/").rsplit("/", 1)[-1],
            job_url=url,
            description=raw.get("description"),
        )
