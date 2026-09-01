"""Canonical job schema used by all sources and storage backends."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from typing import Any, ClassVar

from .text import MISSING, canonical_url, clean_text, stable_fallback_id, strip_html


@dataclass(frozen=True, slots=True)
class Job:
    title: str
    company_name: str
    sector: str
    location: str
    contract_type: str
    education_level: str
    experience_years: str
    job_level: str
    profession: str
    open_positions: str
    work_mode: str
    published_date: str
    published_time_utc: str
    job_alias: str
    job_id: str
    job_url: str
    description: str
    source: str
    provider_job_id: str
    added_at: str = ""

    HEADERS: ClassVar[tuple[str, ...]] = (
        "title", "company_name", "sector", "location", "contract_type",
        "education_level", "experience_years", "job_level", "profession",
        "open_positions", "work_mode", "published_date", "published_time_utc",
        "job_alias", "job_id", "job_url", "description", "source",
        "provider_job_id", "added_at",
    )

    @classmethod
    def create(cls, *, source: str, job_id: Any = "", **values: Any) -> "Job":
        normalized_source = clean_text(source).lower()
        if not normalized_source:
            raise ValueError("source is required")
        normalized_url = canonical_url(values.get("job_url"))
        normalized_title = clean_text(values.get("title")) or MISSING
        normalized_company = clean_text(values.get("company_name")) or MISSING
        normalized_location = clean_text(values.get("location")) or MISSING
        normalized_id = clean_text(job_id) or stable_fallback_id(
            normalized_source,
            (normalized_url, normalized_title, normalized_company, normalized_location),
        )

        defaults = {
            name: MISSING
            for name in cls.HEADERS
            if name not in {"source", "provider_job_id", "added_at"}
        }
        defaults.update(values)
        defaults.update(
            title=normalized_title,
            company_name=normalized_company,
            location=normalized_location,
            job_id=normalized_id,
            job_url=normalized_url or MISSING,
            description=strip_html(values.get("description")) or MISSING,
            source=normalized_source,
            provider_job_id=f"{normalized_source}:{normalized_id}",
            added_at=clean_text(values.get("added_at")),
        )
        for key, value in tuple(defaults.items()):
            if key not in {"description", "source", "provider_job_id", "added_at"}:
                defaults[key] = clean_text(value) or MISSING
        return cls(**{name: defaults[name] for name in cls.HEADERS})

    def with_added_at(self, now: datetime | None = None) -> "Job":
        if self.added_at:
            return self
        timestamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        return replace(self, added_at=timestamp.replace(microsecond=0).isoformat().replace("+00:00", "Z"))

    def as_row(self) -> list[str]:
        values = asdict(self.with_added_at())
        return [values[name] for name in self.HEADERS]
