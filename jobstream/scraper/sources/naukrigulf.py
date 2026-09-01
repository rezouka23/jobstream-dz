"""NaukriGulf Algeria search API adapter."""

from __future__ import annotations

import time
from typing import Any

import requests

from ..schema import Job
from ..text import MISSING, clean_text, utc_parts


class NaukriGulfAdapter:
    name = "naukrigulf"
    api_url = "https://www.naukrigulf.com/spapi/jobapi/search"
    page_size = 30
    headers = {
        "accept": "application/json",
        "accept-language": "ENGLISH",
        "client-type": "desktop",
        "device-type": "desktop",
        "referer": "https://www.naukrigulf.com/jobs-in-algeria",
    }

    def __init__(self, session: requests.Session, *, timeout: int = 30, delay: float = 0.2):
        self.session = session
        self.timeout = timeout
        self.delay = delay

    def fetch(self) -> list[Job]:
        raw_jobs: list[dict[str, Any]] = []
        offset = 0
        page = 1
        while True:
            payload = self._fetch_page(offset, page)
            page_jobs = payload.get("jobs") or []
            if not page_jobs:
                break
            raw_jobs.extend(page_jobs)
            offset += self.page_size
            if offset >= int(payload.get("totalJobsCount") or len(raw_jobs)):
                break
            page += 1
            if self.delay:
                time.sleep(self.delay)
        return [self.normalize(item) for item in raw_jobs]

    def _fetch_page(self, offset: int, page: int) -> dict[str, Any]:
        response = self.session.get(
            self.api_url,
            params={
                "Freshness": 1,
                "Keywords": "",
                "Limit": self.page_size,
                "Location": "algeria",
                "Offset": offset,
                "SortPreference": "relevance",
                "pageNo": page,
                "seo": 1,
            },
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _experience(value: Any) -> str:
        if not isinstance(value, dict):
            return MISSING
        minimum = clean_text(value.get("min"))
        maximum = clean_text(value.get("max"))
        if minimum and maximum:
            return f"{minimum} years" if minimum == maximum else f"{minimum}-{maximum} years"
        if minimum:
            return f"{minimum}+ years"
        if maximum:
            return f"Up to {maximum} years"
        return MISSING

    @classmethod
    def normalize(cls, raw: dict[str, Any]) -> Job:
        company = raw.get("company") or {}
        published_date, published_time = utc_parts(raw.get("latestPostedDate"))
        relative_url = clean_text(raw.get("jdURL"))
        job_url = relative_url if relative_url.startswith(("http://", "https://")) else (
            f"https://www.naukrigulf.com/{relative_url.lstrip('/')}" if relative_url else ""
        )
        return Job.create(
            source=cls.name,
            job_id=raw.get("jobId"),
            title=raw.get("designation"),
            company_name=company.get("name"),
            location=raw.get("location"),
            experience_years=cls._experience(raw.get("experience")),
            profession=raw.get("keywords") or raw.get("whitelistedkeywords"),
            open_positions=raw.get("vacancies"),
            published_date=published_date,
            published_time_utc=published_time,
            job_alias=relative_url,
            job_url=job_url,
            description=raw.get("description") or raw.get("jobInfo"),
        )
