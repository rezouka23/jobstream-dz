"""Emploitic public API adapter."""

from __future__ import annotations

import re
import time
from typing import Any

import requests

from ..schema import Job
from ..text import MISSING, clean_text, labels, slugify, utc_parts


class EmploiticAdapter:
    name = "emploitic"
    api_url = "https://emploitic.com/api/v4/jobs"

    def __init__(self, session: requests.Session, *, timeout: int = 30, delay: float = 0.2):
        self.session = session
        self.timeout = timeout
        self.delay = delay

    def fetch(self) -> list[Job]:
        first = self._fetch_page(1)
        pages = int((first.get("pagination") or {}).get("totalPages") or 1)
        raw_jobs = list(first.get("results") or [])
        for page in range(2, pages + 1):
            if self.delay:
                time.sleep(self.delay)
            raw_jobs.extend(self._fetch_page(page).get("results") or [])
        return [self.normalize(item) for item in raw_jobs]

    def _fetch_page(self, page: int) -> dict[str, Any]:
        response = self.session.get(
            self.api_url,
            params={
                "sort[0]": "publishedAt_timestamp:desc",
                "pagination[page]": page,
                "pagination[pageSize]": 100,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def normalize(cls, raw: dict[str, Any]) -> Job:
        company = raw.get("company") or {}
        criteria = raw.get("criteria") or {}
        sector = clean_text((company.get("sector") or {}).get("label"))
        company_name = clean_text(company.get("name") or criteria.get("alternativeCompanyName"))
        if not company_name and raw.get("isAnonymous") is True:
            company_name = "Anonymous employer"
        arn_match = re.search(r"job:([^:]+)$", clean_text(raw.get("arn")))
        job_id = arn_match.group(1) if arn_match else ""
        published_date, published_time = utc_parts(raw.get("publishedAt"))
        alias = clean_text(raw.get("alias"))
        company_alias = clean_text(company.get("alias"))
        job_url = ""
        if company_alias and sector and alias:
            job_url = (
                f"https://emploitic.com/entreprises/{company_alias}/offres-d-emploi/"
                f"{slugify(sector)}/{alias}"
            )
        return Job.create(
            source=cls.name,
            job_id=job_id,
            title=raw.get("title"),
            company_name=company_name,
            sector=sector,
            location=labels(criteria.get("location")),
            contract_type=labels(criteria.get("contractType")),
            education_level=labels(criteria.get("educationLevel")),
            experience_years=labels(criteria.get("experienceYears")),
            job_level=labels(criteria.get("jobLevel")),
            profession=labels(criteria.get("profession")),
            open_positions=raw.get("openPositions"),
            work_mode=raw.get("workMode"),
            published_date=published_date,
            published_time_utc=published_time,
            job_alias=alias or MISSING,
            job_url=job_url,
            description=raw.get("description"),
        )
