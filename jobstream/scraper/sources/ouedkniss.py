"""Ouedkniss jobs GraphQL adapter."""

from __future__ import annotations

import time
from typing import Any

import requests

from ..schema import Job
from ..text import clean_text, utc_parts

QUERY = """
query SearchQuery($filter: SearchFilterInput) {
  search(filter: $filter) {
    announcements {
      data { id title slug createdAt: refreshedAt description cities { name }
             store { name } category { slug } }
      paginatorInfo { lastPage hasMorePages }
    }
  }
}
"""


class OuedknissAdapter:
    name = "ouedkniss"
    api_url = "https://api.ouedkniss.com/graphql"

    def __init__(
        self,
        session: requests.Session,
        *,
        timeout: int = 30,
        delay: float = 0.2,
        max_pages: int = 20,
    ):
        self.session = session
        self.timeout = timeout
        self.delay = delay
        self.max_pages = max_pages

    def fetch(self) -> list[Job]:
        first = self._fetch_page(1)
        announcements = self._announcements(first)
        jobs = [self.normalize(item) for item in announcements.get("data") or []]
        last_page = min(int((announcements.get("paginatorInfo") or {}).get("lastPage") or 1), self.max_pages)
        for page in range(2, last_page + 1):
            if self.delay:
                time.sleep(self.delay)
            items = self._announcements(self._fetch_page(page)).get("data") or []
            if not items:
                break
            jobs.extend(self.normalize(item) for item in items)
        return jobs

    def _fetch_page(self, page: int) -> dict[str, Any]:
        response = self.session.post(
            self.api_url,
            headers={
                "accept-language": "fr",
                "content-type": "application/json",
                "locale": "fr",
                "origin": "https://www.ouedkniss.com",
                "referer": "https://www.ouedkniss.com/",
            },
            json={
                "operationName": "SearchQuery",
                "variables": {"filter": {
                    "categorySlug": "emploi_offres", "page": page,
                    "count": 48, "orderByField": {"field": "REFRESHED_AT"},
                }},
                "query": QUERY,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("errors"):
            raise RuntimeError(f"Ouedkniss GraphQL returned {len(payload['errors'])} error(s)")
        return payload

    @staticmethod
    def _announcements(payload: dict[str, Any]) -> dict[str, Any]:
        return (((payload.get("data") or {}).get("search") or {}).get("announcements") or {})

    @classmethod
    def normalize(cls, raw: dict[str, Any]) -> Job:
        published_date, published_time = utc_parts(raw.get("createdAt"))
        locations = " | ".join(
            name
            for item in (raw.get("cities") or [])
            if isinstance(item, dict) and (name := clean_text(item.get("name")))
        )
        category_slug = clean_text((raw.get("category") or {}).get("slug"))
        sector = category_slug.removeprefix("emploi_offres-").replace("-", " ")
        slug = clean_text(raw.get("slug"))
        job_id = clean_text(raw.get("id"))
        return Job.create(
            source=cls.name,
            job_id=job_id,
            title=raw.get("title"),
            company_name=(raw.get("store") or {}).get("name"),
            sector=sector,
            location=locations,
            profession=sector,
            published_date=published_date,
            published_time_utc=published_time,
            job_alias=slug,
            job_url=f"https://www.ouedkniss.com/{slug}-d{job_id}" if slug and job_id else "",
            description=raw.get("description"),
        )
