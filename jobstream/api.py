from __future__ import annotations

import os
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from threading import Lock
from typing import Any
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

from .cv_matcher import CVProfileError, extract_candidate_profile, rank_jobs_for_profile
from .cv_parser import CVParseError, extract_cv_text
from .sheets import extract_apply_url, fetch_sheet_rows, fingerprint_job, get_sheets_service


REPO_ROOT = Path(__file__).resolve().parent.parent
LANDING_DIR = REPO_ROOT / "landing"
CV_MATCH_DIR = REPO_ROOT / "cv-match"
ALGERIA_TZ = ZoneInfo("Africa/Algiers")
SHEET_END_COL = "Z"

_rate_limit_hits: dict[str, list[float]] = {}
_rate_limit_lock = Lock()


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv()


def _env_int(
    name: str, default: int, *, minimum: int = 1, maximum: int | None = None
) -> int:
    try:
        value = int(os.getenv(name, "") or default)
    except ValueError:
        value = default
    value = max(minimum, value)
    return min(value, maximum) if maximum is not None else value


def _sheet_config() -> tuple[str, str]:
    spreadsheet_id = os.getenv("SPREADSHEET_ID", "").strip()
    sheet_name = os.getenv("SHEET_NAME", "jobs").strip()
    if not spreadsheet_id:
        raise HTTPException(status_code=500, detail="SPREADSHEET_ID is not configured")
    if not sheet_name:
        raise HTTPException(status_code=500, detail="SHEET_NAME is not configured")
    return spreadsheet_id, sheet_name


def _fetch_rows(*, max_rows: int) -> list[dict[str, str]]:
    spreadsheet_id, sheet_name = _sheet_config()
    try:
        return fetch_sheet_rows(
            service=get_sheets_service(),
            spreadsheet_id=spreadsheet_id,
            sheet_name=sheet_name,
            max_rows=max_rows,
            end_col=SHEET_END_COL,
        )
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        get_sheets_service.cache_clear()
        raise HTTPException(
            status_code=503,
            detail="Google Sheets job data is temporarily unavailable. Try again later.",
        ) from exc


def _to_text(value: Any, *, default: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text or default


def _parse_iso_datetime(value: Any) -> datetime | None:
    text = _to_text(value)
    if not text or text.lower() in {"-", "n/a", "none", "not specified", "null", "unknown"}:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed


def _parse_date(value: Any) -> date | None:
    text = _to_text(value)
    for date_format in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, date_format).date()
        except ValueError:
            continue
    return None


def _row_arrival_date(row: dict[str, str]) -> tuple[date | None, str]:
    for field in ("added_at", "scraped_at"):
        timestamp = _parse_iso_datetime(row.get(field))
        if timestamp is not None:
            return timestamp.astimezone(ALGERIA_TZ).date(), field
        day = _parse_date(row.get(field))
        if day is not None:
            return day, field
    return _parse_date(row.get("published_date")), "published_date"


def _source_from_url(url: str) -> str:
    host = urlsplit(url).netloc.lower()
    known_sources = {
        "linkedin": "LinkedIn",
        "emploitic": "Emploitic",
        "naukrigulf": "NaukriGulf",
        "jobindz": "Jobindz",
        "ouedkniss": "Ouedkniss",
    }
    return next((label for token, label in known_sources.items() if token in host), "unknown")


def _public_job(
    row: dict[str, str], *, arrival_date: date, date_basis: str, matchable: bool = False
) -> dict[str, str]:
    apply_url = extract_apply_url(row)
    job = {
        "id": fingerprint_job(row),
        "source": _to_text(row.get("source")) or _source_from_url(apply_url),
        "title": _to_text(row.get("title"), default="Not specified"),
        "company_name": _to_text(row.get("company_name"), default="Not specified"),
        "location": _to_text(row.get("location"), default="Not specified"),
        "apply_url": apply_url,
        "published_date": _to_text(row.get("published_date"), default="Not specified"),
        "published_time_utc": _to_text(row.get("published_time_utc"), default="Not specified"),
        "added_at": _to_text(row.get("added_at") or row.get("scraped_at")),
        "arrival_date": arrival_date.isoformat(),
        "date_basis": date_basis,
    }
    if matchable:
        job.update(
            {
                field: _to_text(row.get(field))
                for field in (
                    "sector",
                    "contract_type",
                    "education_level",
                    "experience_years",
                    "job_level",
                    "profession",
                    "work_mode",
                    "description",
                )
            }
        )
    return job


def _recent_jobs_payload(*, days: int, limit: int, matchable: bool = False) -> dict[str, Any]:
    now = datetime.now(ALGERIA_TZ)
    window_end = now.date()
    window_start = window_end - timedelta(days=days - 1)
    rows = _fetch_rows(max_rows=_env_int("JOBS_MAX_ROWS", 1000, minimum=25, maximum=5000))
    jobs: list[dict[str, str]] = []
    seen: set[str] = set()
    skipped_without_links = 0
    skipped_outside_window = 0
    skipped_duplicates = 0

    for row in rows:
        if not extract_apply_url(row):
            skipped_without_links += 1
            continue
        arrival_date, date_basis = _row_arrival_date(row)
        if arrival_date is None or not window_start <= arrival_date <= window_end:
            skipped_outside_window += 1
            continue
        fingerprint = fingerprint_job(row)
        if fingerprint in seen:
            skipped_duplicates += 1
            continue
        seen.add(fingerprint)
        jobs.append(
            _public_job(
                row,
                arrival_date=arrival_date,
                date_basis=date_basis,
                matchable=matchable,
            )
        )
        if limit and len(jobs) >= limit:
            break

    return {
        "date": window_end.isoformat(),
        "timezone": "Africa/Algiers",
        "generated_at": now.astimezone(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "sheet_name": _sheet_config()[1],
        "job_count": len(jobs),
        "jobs": jobs,
        "meta": {
            "days": days,
            "date_window_start": window_start.isoformat(),
            "date_window_end": window_end.isoformat(),
            "scanned_rows": len(rows),
            "skipped_without_links": skipped_without_links,
            "skipped_outside_window": skipped_outside_window,
            "skipped_duplicates": skipped_duplicates,
        },
    }


def _client_ip(request: Request) -> str:
    forwarded_for = _to_text(request.headers.get("x-forwarded-for"))
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip() or "unknown"
    real_ip = _to_text(request.headers.get("x-real-ip"))
    if real_ip:
        return real_ip
    return request.client.host if request.client and request.client.host else "unknown"


def _enforce_rate_limit(request: Request) -> None:
    limit = _env_int("CV_MATCH_RATE_LIMIT_REQUESTS", 3, minimum=0, maximum=100)
    if limit == 0:
        return
    window = _env_int(
        "CV_MATCH_RATE_LIMIT_WINDOW_SECONDS", 3600, minimum=60, maximum=86400
    )
    now = time.monotonic()
    client_ip = _client_ip(request)
    with _rate_limit_lock:
        hits = [hit for hit in _rate_limit_hits.get(client_ip, []) if hit > now - window]
        if len(hits) >= limit:
            retry_after = max(1, int(hits[0] + window - now))
            _rate_limit_hits[client_ip] = hits
            raise HTTPException(
                status_code=429,
                detail="Too many CV match requests. Try again later.",
                headers={"Retry-After": str(retry_after)},
            )
        _rate_limit_hits[client_ip] = [*hits, now]


def _public_match(job: dict[str, Any]) -> dict[str, Any]:
    public_fields = (
        "id",
        "source",
        "title",
        "company_name",
        "location",
        "apply_url",
        "published_date",
        "published_time_utc",
        "added_at",
        "arrival_date",
        "date_basis",
    )
    return {
        **{field: _to_text(job.get(field)) for field in public_fields},
        "score": int(job.get("score", 0)),
        "reasons": [str(reason) for reason in job.get("reasons", []) if str(reason).strip()][
            :5
        ],
    }


_load_dotenv()
app = FastAPI(title="JobStream DZ API", version="0.1.0")

if LANDING_DIR.is_dir():
    app.mount("/landing", StaticFiles(directory=LANDING_DIR, html=True), name="landing")
if CV_MATCH_DIR.is_dir():
    app.mount("/cv-match", StaticFiles(directory=CV_MATCH_DIR, html=True), name="cv-match")


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    if not LANDING_DIR.is_dir():
        raise HTTPException(status_code=404, detail="Landing directory not found")
    return RedirectResponse(url="/landing/", status_code=307)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/feed/latest")
def latest_feed() -> dict[str, Any]:
    return _recent_jobs_payload(
        days=_env_int("FEED_DAYS", 7, minimum=1, maximum=30),
        limit=_env_int("FEED_LIMIT", 10, minimum=1, maximum=100),
    )


@app.get("/api/jobs/today")
def jobs_today(days: int = Query(1, ge=1, le=30)) -> dict[str, Any]:
    max_days = _env_int("JOBS_MAX_DAYS", 7, minimum=1, maximum=30)
    return _recent_jobs_payload(
        days=min(days, max_days),
        limit=_env_int("JOBS_LIMIT", 150, minimum=1, maximum=500),
    )


@app.post("/api/cv/match")
async def cv_match(request: Request, cv: UploadFile = File(...)) -> dict[str, Any]:
    _enforce_rate_limit(request)
    max_mb = _env_int("CV_MATCH_MAX_FILE_MB", 5, minimum=1, maximum=25)
    max_bytes = max_mb * 1024 * 1024
    data = await cv.read(max_bytes + 1)
    if not data:
        raise HTTPException(status_code=400, detail="Upload a CV file to find matches.")
    if len(data) > max_bytes:
        raise HTTPException(status_code=400, detail=f"CV file is too large. Maximum size is {max_mb} MB.")

    try:
        cv_text = await run_in_threadpool(
            extract_cv_text, filename=cv.filename or "", data=data
        )
    except CVParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    jobs_payload = await run_in_threadpool(
        _recent_jobs_payload,
        days=_env_int("CV_MATCH_DAYS", 7, minimum=1, maximum=30),
        limit=0,
        matchable=True,
    )
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    try:
        profile = await run_in_threadpool(
            extract_candidate_profile,
            cv_text=cv_text,
            api_key=api_key,
            model=os.getenv("CV_MATCH_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini",
            text_char_limit=_env_int(
                "CV_MATCH_TEXT_CHAR_LIMIT", 12000, minimum=1000, maximum=30000
            ),
        )
    except CVProfileError as exc:
        status = 500 if not api_key else 502
        raise HTTPException(
            status_code=status,
            detail="CV profile extraction failed. Try again later.",
        ) from exc

    match_limit = _env_int("CV_MATCH_LIMIT", 20, minimum=1, maximum=100)
    matches = rank_jobs_for_profile(
        profile=profile, jobs=jobs_payload["jobs"], limit=match_limit
    )
    return {
        "candidate_summary": profile,
        "match_count": len(matches),
        "matches": [_public_match(match) for match in matches],
        "meta": {
            **jobs_payload["meta"],
            "model": os.getenv("CV_MATCH_MODEL", "gpt-4o-mini").strip()
            or "gpt-4o-mini",
            "match_limit": match_limit,
        },
    }
