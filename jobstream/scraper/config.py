"""Environment-backed scraper configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_positive_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


@dataclass(frozen=True, slots=True)
class ScraperConfig:
    spreadsheet_id: str
    sheet_name: str
    state_file: Path
    interval_seconds: int
    request_timeout: int
    request_delay: float
    sources: tuple[str, ...]
    linkedin_search_terms: tuple[str, ...]
    linkedin_hours_old: int
    linkedin_results_wanted: int
    linkedin_remote_only: bool

    @classmethod
    def from_env(cls) -> "ScraperConfig":
        source_names = [
            item.strip().lower()
            for item in os.getenv(
                "SCRAPER_SOURCES", "emploitic,naukrigulf,jobindz,ouedkniss"
            ).split(",")
            if item.strip()
        ]
        if _as_bool(os.getenv("SCRAPER_ENABLE_LINKEDIN")) and "linkedin" not in source_names:
            source_names.append("linkedin")

        terms = tuple(
            item.strip()
            for item in os.getenv(
                "LINKEDIN_SEARCH_TERMS",
                "software developer,customer support,marketing,finance",
            ).split(",")
            if item.strip()
        )
        try:
            request_delay = float(os.getenv("SCRAPER_REQUEST_DELAY", "0.2"))
        except ValueError as exc:
            raise ValueError("SCRAPER_REQUEST_DELAY must be numeric") from exc
        if request_delay < 0:
            raise ValueError("SCRAPER_REQUEST_DELAY cannot be negative")

        return cls(
            spreadsheet_id=os.getenv("GOOGLE_SPREADSHEET_ID", "").strip(),
            sheet_name=os.getenv("GOOGLE_SHEET_NAME", "jobs").strip() or "jobs",
            state_file=Path(
                os.getenv("SCRAPER_STATE_FILE", ".jobstream-scraper-state.json")
            ).expanduser(),
            interval_seconds=_as_positive_int("SCRAPER_INTERVAL_SECONDS", 1800),
            request_timeout=_as_positive_int("SCRAPER_REQUEST_TIMEOUT", 30),
            request_delay=request_delay,
            sources=tuple(dict.fromkeys(source_names)),
            linkedin_search_terms=terms,
            linkedin_hours_old=_as_positive_int("LINKEDIN_HOURS_OLD", 168),
            linkedin_results_wanted=_as_positive_int("LINKEDIN_RESULTS_WANTED", 50),
            linkedin_remote_only=_as_bool(os.getenv("LINKEDIN_REMOTE_ONLY")),
        )

    def require_spreadsheet_id(self) -> str:
        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SPREADSHEET_ID is required")
        return self.spreadsheet_id
