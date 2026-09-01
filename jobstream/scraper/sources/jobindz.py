"""Jobindz HTML adapter."""

from __future__ import annotations

import re
import time

import requests
from bs4 import BeautifulSoup, Tag

from ..schema import Job
from ..text import MISSING, clean_text


class JobindzAdapter:
    name = "jobindz"
    base_url = "https://jobindz.com"
    search_url = f"{base_url}/offres"

    def __init__(self, session: requests.Session, *, timeout: int = 30, delay: float = 0.2):
        self.session = session
        self.timeout = timeout
        self.delay = delay

    def fetch(self) -> list[Job]:
        first = self._fetch_page(1)
        jobs, pages = self.parse_page(first)
        for page in range(2, pages + 1):
            if self.delay:
                time.sleep(self.delay)
            page_jobs, _ = self.parse_page(self._fetch_page(page))
            jobs.extend(page_jobs)
        return jobs

    def _fetch_page(self, page: int) -> str:
        response = self.session.get(
            self.search_url,
            params={"page": page, "keyword": ""},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.text

    @classmethod
    def parse_page(cls, html_text: str) -> tuple[list[Job], int]:
        soup = BeautifulSoup(html_text, "html.parser")
        jobs: list[Job] = []
        for card in soup.select("a.offer-card[href]"):
            href = clean_text(card.get("href"))
            slug = href.rstrip("/").rsplit("/", 1)[-1]
            id_match = re.search(r"-([^-]+)$", slug)
            company = cls._text(card.select_one(".offer-company"))
            if company == "-":
                company = "Anonymous employer"
            published_date = MISSING
            date_match = re.search(r"(\d{2})/(\d{2})/(\d{4})", cls._text(card.select_one(".offer-date")))
            if date_match:
                day, month, year = date_match.groups()
                published_date = f"{year}-{month}-{day}"
            positions = cls._meta(card, "fa-users")
            positions_match = re.search(r"\d+", positions)
            profession = cls._meta(card, "fa-briefcase")
            jobs.append(Job.create(
                source=cls.name,
                job_id=id_match.group(1) if id_match else slug,
                title=cls._text(card.select_one(".offer-title")),
                company_name=company,
                sector=profession,
                location=cls._meta(card, "fa-map-marker-alt"),
                contract_type=cls._meta(card, "fa-file-contract"),
                profession=profession,
                open_positions=positions_match.group(0) if positions_match else "",
                published_date=published_date,
                published_time_utc="00:00:00" if published_date != MISSING else MISSING,
                job_alias=slug,
                job_url=f"{cls.base_url}{href}" if href.startswith("/") else href,
            ))
        pages = [
            int(match.group(1))
            for link in soup.select('a[href*="/offres?page="]')
            if (match := re.search(r"[?&]page=(\d+)", clean_text(link.get("href"))))
        ]
        return jobs, max(pages, default=1)

    @staticmethod
    def _text(element: Tag | None) -> str:
        return clean_text(element.get_text(" ", strip=True)) if element else ""

    @classmethod
    def _meta(cls, card: Tag, icon_class: str) -> str:
        for block in card.select(".meta-item"):
            if block.select_one(f".{icon_class}"):
                return cls._text(block.select_one("span"))
        return ""
