from __future__ import annotations

import json
import os
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from threading import Lock
from typing import Any
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from .cv_matcher import CVProfileError, extract_candidate_profile, rank_jobs_for_profile
from .cv_parser import CVParseError, extract_cv_text
from .sheets import build_sheets_service, extract_apply_url, fetch_sheet_rows, fingerprint_job


REPO_ROOT = Path(__file__).resolve().parent.parent
LANDING_DIR = REPO_ROOT / "landing"
JOBS_TODAY_DIR = REPO_ROOT / "jobs-today"
CV_MATCH_DIR = REPO_ROOT / "cv-match"
LOGO_FILE = REPO_ROOT / "logo.png"
LANDING_REFERENCE_FILE = REPO_ROOT / "landing.png"
ALGERIA_TZ = ZoneInfo("Africa/Algiers")
TODAY_SHEET_END_COL = "Z"
CV_MATCH_SHEET_END_COL = "Z"

_today_jobs_cache: dict[int, dict[str, Any]] = {}
_recent_jobs_cache: dict[tuple[str, int], tuple[float, dict[str, Any]]] = {}
_recent_jobs_cache_lock = Lock()
_sheets_service: Any | None = None
_cv_match_rate_limit_hits: dict[str, list[float]] = {}
_cv_match_rate_limit_lock = Lock()


def _load_dotenv_if_available() -> None:
    try:
        from dotenv import load_dotenv
    except Exception:
        return
    load_dotenv()


def _to_text(value: Any, *, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    if text:
        return text
    return default


def _latest_digest_path() -> Path:
    return Path(os.getenv("LATEST_DIGEST_FILE", "latest_digest.json")).expanduser()


def _digest_history_dir() -> Path:
    return Path(os.getenv("DIGESTS_DIR", "digest_history")).expanduser()


def _feed_limit() -> int:
    raw = os.getenv("FEED_LIMIT", "10").strip()
    try:
        return max(1, min(25, int(raw)))
    except ValueError:
        return 10


def _env_int(name: str, default: int, *, minimum: int = 1, maximum: int | None = None) -> int:
    raw = os.getenv(name, "").strip()
    try:
        value = int(raw) if raw else default
    except ValueError:
        value = default

    value = max(minimum, value)
    if maximum is not None:
        value = min(maximum, value)
    return value


def _today_jobs_max_rows() -> int:
    return _env_int("TODAY_JOBS_MAX_ROWS", 1000, minimum=25, maximum=5000)


def _today_jobs_limit() -> int:
    return _env_int("TODAY_JOBS_LIMIT", 150, minimum=1, maximum=500)


def _today_jobs_cache_seconds() -> int:
    return _env_int("TODAY_JOBS_CACHE_SECONDS", 120, minimum=0, maximum=900)


def _today_jobs_max_days() -> int:
    return _env_int("TODAY_JOBS_MAX_DAYS", 7, minimum=1, maximum=30)


def _cv_match_max_rows() -> int:
    return _env_int("CV_MATCH_MAX_ROWS", 1000, minimum=25, maximum=5000)


def _cv_match_limit() -> int:
    return _env_int("CV_MATCH_LIMIT", 20, minimum=1, maximum=100)


def _cv_match_days() -> int:
    return _env_int("CV_MATCH_DAYS", 7, minimum=1, maximum=30)


def _cv_match_max_file_mb() -> int:
    return _env_int("CV_MATCH_MAX_FILE_MB", 5, minimum=1, maximum=25)


def _cv_match_text_char_limit() -> int:
    return _env_int("CV_MATCH_TEXT_CHAR_LIMIT", 12000, minimum=1000, maximum=30000)


def _cv_match_rate_limit_requests() -> int:
    return _env_int("CV_MATCH_RATE_LIMIT_REQUESTS", 3, minimum=0, maximum=100)


def _cv_match_rate_limit_window_seconds() -> int:
    return _env_int("CV_MATCH_RATE_LIMIT_WINDOW_SECONDS", 3600, minimum=60, maximum=86400)


def _cv_match_model() -> str:
    return os.getenv("CV_MATCH_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"


def _openai_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "").strip()


def _sheet_name() -> str:
    return os.getenv("SHEET_NAME", "emploitic_jobs_all_algeria_clean").strip() or "emploitic_jobs_all_algeria_clean"


def _spreadsheet_id() -> str:
    spreadsheet_id = os.getenv("SPREADSHEET_ID", "").strip()
    if not spreadsheet_id:
        raise HTTPException(status_code=500, detail="SPREADSHEET_ID is not configured")
    return spreadsheet_id


def _load_service_account_json(raw: str) -> dict[str, Any]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500, detail="GOOGLE_SERVICE_ACCOUNT_JSON is invalid"
        ) from exc

    private_key = data.get("private_key")
    if isinstance(private_key, str):
        data["private_key"] = private_key.replace("\\n", "\n")
    return data


def _jobs_sheet_service() -> Any:
    global _sheets_service

    if _sheets_service is not None:
        return _sheets_service

    service_account_json_raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    service_account_file_raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "").strip()

    service_account_json = None
    service_account_file = None
    if service_account_json_raw:
        service_account_json = _load_service_account_json(service_account_json_raw)
    elif service_account_file_raw:
        service_account_file = str(Path(service_account_file_raw).expanduser())
    else:
        raise HTTPException(status_code=500, detail="Google Sheets credentials are not configured")

    _sheets_service = build_sheets_service(
        service_account_file=service_account_file,
        service_account_json=service_account_json,
    )
    return _sheets_service


def _read_latest_digest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise HTTPException(status_code=404, detail="No published digest yet")

    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500, detail="Latest digest file is invalid"
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=500, detail="Failed to read latest digest"
        ) from exc

    if not isinstance(payload, dict):
        raise HTTPException(status_code=500, detail="Latest digest payload is invalid")

    return payload


def _public_job(job: dict[str, Any]) -> dict[str, str]:
    return {
        "id": _to_text(job.get("id"), default="unknown"),
        "source": _to_text(job.get("source"), default="unknown"),
        "title": _to_text(job.get("title"), default="Not specified"),
        "company_name": _to_text(job.get("company_name"), default="Not specified"),
        "location": _to_text(job.get("location"), default="Not specified"),
        "apply_url": _to_text(job.get("apply_url"), default=""),
        "contract_type": _to_text(job.get("contract_type")),
        "experience_years": _to_text(job.get("experience_years")),
        "job_level": _to_text(job.get("job_level")),
        "work_mode": _to_text(job.get("work_mode")),
        "published_date": _to_text(job.get("published_date"), default="Not specified"),
        "published_time_utc": _to_text(
            job.get("published_time_utc"), default="Not specified"
        ),
    }


def _source_from_url(url: str) -> str:
    host = urlsplit(url).netloc.lower()
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
    if "ouedkniss" in host:
        return "Ouedkniss"
    return "unknown"


def _public_sheet_job(job: dict[str, str], *, date_basis: str, arrival_date: str) -> dict[str, str]:
    apply_url = extract_apply_url(job)
    source = _to_text(job.get("source"), default="") or _source_from_url(apply_url)
    fingerprint = fingerprint_job(job)
    return {
        "id": fingerprint,
        "source": source,
        "title": _to_text(job.get("title"), default="Not specified"),
        "company_name": _to_text(job.get("company_name"), default="Not specified"),
        "location": _to_text(job.get("location"), default="Not specified"),
        "apply_url": apply_url,
        "published_date": _to_text(job.get("published_date"), default="Not specified"),
        "published_time_utc": _to_text(job.get("published_time_utc"), default="Not specified"),
        "added_at": _to_text(job.get("added_at") or job.get("scraped_at"), default=""),
        "arrival_date": arrival_date,
        "date_basis": date_basis,
        "contract_type": _to_text(job.get("contract_type")),
        "experience_years": _to_text(job.get("experience_years")),
        "job_level": _to_text(job.get("job_level")),
        "work_mode": _to_text(job.get("work_mode")),
    }


def _matchable_sheet_job(job: dict[str, str], *, date_basis: str, arrival_date: str) -> dict[str, str]:
    public_job = _public_sheet_job(job, date_basis=date_basis, arrival_date=arrival_date)
    return {
        **public_job,
        "sector": _to_text(job.get("sector"), default=""),
        "contract_type": _to_text(job.get("contract_type"), default=""),
        "education_level": _to_text(job.get("education_level"), default=""),
        "experience_years": _to_text(job.get("experience_years"), default=""),
        "job_level": _to_text(job.get("job_level"), default=""),
        "profession": _to_text(job.get("profession"), default=""),
        "work_mode": _to_text(job.get("work_mode"), default=""),
        "description": _to_text(job.get("description"), default=""),
    }


def _parse_iso_datetime(value: str) -> datetime | None:
    text = _to_text(value)
    if not text or text.lower() in {"not specified", "unknown", "n/a", "none", "null", "-"}:
        return None

    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _parse_date(value: str) -> date | None:
    text = _to_text(value)
    if not text or text.lower() in {"not specified", "unknown", "n/a", "none", "null", "-"}:
        return None

    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def _row_arrival_date(row: dict[str, str]) -> tuple[date | None, str]:
    for field in ("added_at", "scraped_at"):
        timestamp = _parse_iso_datetime(row.get(field, ""))
        if timestamp is not None:
            return timestamp.astimezone(ALGERIA_TZ).date(), field

        day = _parse_date(row.get(field, ""))
        if day is not None:
            return day, field

    published_day = _parse_date(row.get("published_date", ""))
    if published_day is not None:
        return published_day, "published_date"

    return None, ""


def _request_client_ip(request: Request) -> str:
    forwarded_for = _to_text(request.headers.get("x-forwarded-for"))
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip() or "unknown"

    real_ip = _to_text(request.headers.get("x-real-ip"))
    if real_ip:
        return real_ip

    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def _enforce_cv_match_rate_limit(request: Request) -> None:
    limit = _cv_match_rate_limit_requests()
    if limit <= 0:
        return

    window_seconds = _cv_match_rate_limit_window_seconds()
    now = time.time()
    window_start = now - window_seconds
    client_ip = _request_client_ip(request)

    with _cv_match_rate_limit_lock:
        hits = [hit for hit in _cv_match_rate_limit_hits.get(client_ip, []) if hit > window_start]
        if len(hits) >= limit:
            retry_after = max(1, int(hits[0] + window_seconds - now))
            _cv_match_rate_limit_hits[client_ip] = hits
            raise HTTPException(
                status_code=429,
                detail="Too many CV match requests. Please try again later.",
                headers={"Retry-After": str(retry_after)},
            )

        hits.append(now)
        _cv_match_rate_limit_hits[client_ip] = hits


def _row_arrival_timestamp(row: dict[str, str]) -> tuple[datetime | None, str]:
    """Resolve precise collection time, using local midnight for date-only rows."""
    for field in ("added_at", "scraped_at"):
        value = _to_text(row.get(field))
        day = _parse_date(value)
        if day is not None:
            return datetime.combine(day, datetime.min.time(), tzinfo=ALGERIA_TZ), field
        stamp = _parse_iso_datetime(value)
        if stamp is not None:
            return stamp.astimezone(ALGERIA_TZ), field

    value = _to_text(row.get("published_date"))
    day = _parse_date(value)
    if day is None:
        return _parse_iso_datetime(value), "published_date"
    published_time = _to_text(row.get("published_time_utc")).removesuffix(" UTC")
    if published_time:
        stamp = _parse_iso_datetime(f"{day.isoformat()}T{published_time}")
        if stamp is not None:
            return stamp.astimezone(ALGERIA_TZ), "published_date"
    return datetime.combine(day, datetime.min.time(), tzinfo=ALGERIA_TZ), "published_date"


def _rolling_recent_payload(payload: dict[str, Any], now: datetime) -> dict[str, Any]:
    """Recheck cached jobs against the moving cutoff without another sheet read."""
    cutoff = now - timedelta(hours=24)
    jobs = [job for job in payload["jobs"]
            if (stamp := _parse_iso_datetime(job.get("arrival_at", ""))) is not None
            and cutoff <= stamp <= now]
    return {
        **payload,
        "job_count": len(jobs),
        "jobs": jobs,
        "meta": {
            **payload["meta"],
            "hours": 24,
            "window_type": "rolling",
            "date_window_start": cutoff.date().isoformat(),
            "date_window_end": now.date().isoformat(),
            "window_start_utc": cutoff.astimezone(timezone.utc).isoformat(),
            "window_end_utc": now.astimezone(timezone.utc).isoformat(),
            "skipped_outside_window": payload["meta"]["skipped_outside_window"] + len(payload["jobs"]) - len(jobs),
        },
    }


def _today_payload(*, days: int = 1, scan_all: bool = False, hours: int | None = None) -> dict[str, Any]:
    now = datetime.now(ALGERIA_TZ)
    today = now.date()
    window_start = today - timedelta(days=days - 1)
    service = _jobs_sheet_service()
    rows = fetch_sheet_rows(
        service=service,
        spreadsheet_id=_spreadsheet_id(),
        sheet_name=_sheet_name(),
        max_rows=None if scan_all else _today_jobs_max_rows(),
        end_col=TODAY_SHEET_END_COL,
    )

    jobs: list[dict[str, str]] = []
    seen: set[str] = set()
    skipped_without_links = 0
    skipped_outside_window = 0
    backfilled = 0

    for row in rows:
        apply_url = extract_apply_url(row)
        if not apply_url:
            skipped_without_links += 1
            continue

        arrival_at = None
        if hours is not None:
            arrival_at, date_basis = _row_arrival_timestamp(row)
            if arrival_at is None or not now - timedelta(hours=hours) <= arrival_at <= now:
                skipped_outside_window += 1
                continue
            arrival_date = arrival_at.astimezone(ALGERIA_TZ).date()
        else:
            arrival_date, date_basis = _row_arrival_date(row)
            if arrival_date is None or arrival_date < window_start or arrival_date > today:
                skipped_outside_window += 1
                continue

        fingerprint = fingerprint_job(row)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        if date_basis == "published_date":
            backfilled += 1
        jobs.append(
            _public_sheet_job(
                row,
                date_basis=date_basis,
                arrival_date=arrival_date.isoformat(),
            )
        )
        if arrival_at is not None:
            jobs[-1]["arrival_at"] = arrival_at.astimezone(timezone.utc).isoformat()
        if not scan_all and len(jobs) >= _today_jobs_limit():
            break

    if scan_all:
        jobs.sort(key=lambda job: (
            _parse_iso_datetime(job.get("arrival_at", "")) or _parse_iso_datetime(job["added_at"]) or
            datetime.fromisoformat(job["arrival_date"]).replace(tzinfo=ALGERIA_TZ)
        ).timestamp(), reverse=True)

    return {
        "date": today.isoformat(),
        "timezone": "Africa/Algiers",
        "generated_at": now.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "sheet_name": _sheet_name(),
        "job_count": len(jobs),
        "jobs": jobs,
        "meta": {
            "basis": "added_at_or_published_date_fallback",
            "days": days if hours is None else hours // 24,
            "date_window_start": window_start.isoformat(),
            "date_window_end": today.isoformat(),
            "backfilled_from_published_date": backfilled,
            "skipped_without_links": skipped_without_links,
            "skipped_outside_today": skipped_outside_window if days == 1 else 0,
            "skipped_outside_window": skipped_outside_window,
            "max_rows": None if scan_all else _today_jobs_max_rows(),
            "scanned_rows": len(rows),
        },
    }


def _cached_today_payload(*, days: int = 1) -> dict[str, Any]:
    cache_seconds = _today_jobs_cache_seconds()
    now = time.time()
    cached = _today_jobs_cache.get(days)
    if cache_seconds > 0 and cached is not None and cached["payload"] is not None and now < cached["expires_at"]:
        return cached["payload"]

    payload = _today_payload(days=days)
    _today_jobs_cache[days] = {"payload": payload, "expires_at": now + cache_seconds}
    return payload


def _cv_match_job_window() -> tuple[date, date]:
    today = datetime.now(ALGERIA_TZ).date()
    start = today - timedelta(days=_cv_match_days() - 1)
    return start, today


def _fetch_cv_match_sheet_rows() -> list[dict[str, str]]:
    global _sheets_service

    last_error: Exception | None = None
    for attempt in range(2):
        try:
            service = _jobs_sheet_service()
            return fetch_sheet_rows(
                service=service,
                spreadsheet_id=_spreadsheet_id(),
                sheet_name=_sheet_name(),
                max_rows=_cv_match_max_rows(),
                end_col=CV_MATCH_SHEET_END_COL,
            )
        except HTTPException:
            raise
        except Exception as exc:
            last_error = exc
            _sheets_service = None
            if attempt == 0:
                time.sleep(0.5)

    raise HTTPException(
        status_code=503,
        detail="Google Sheets job data is temporarily unavailable. Please try again later.",
    ) from last_error


def _cv_match_jobs_payload() -> dict[str, Any]:
    window_start, window_end = _cv_match_job_window()
    rows = _fetch_cv_match_sheet_rows()

    jobs: list[dict[str, str]] = []
    seen: set[str] = set()
    skipped_without_links = 0
    skipped_outside_window = 0
    skipped_duplicates = 0
    backfilled = 0

    for row in rows:
        apply_url = extract_apply_url(row)
        if not apply_url:
            skipped_without_links += 1
            continue

        arrival_date, date_basis = _row_arrival_date(row)
        if arrival_date is None or arrival_date < window_start or arrival_date > window_end:
            skipped_outside_window += 1
            continue

        fingerprint = fingerprint_job(row)
        if fingerprint in seen:
            skipped_duplicates += 1
            continue
        seen.add(fingerprint)
        if date_basis == "published_date":
            backfilled += 1
        jobs.append(
            _matchable_sheet_job(
                row,
                date_basis=date_basis,
                arrival_date=arrival_date.isoformat(),
            )
        )

    return {
        "jobs": jobs,
        "meta": {
            "sheet_name": _sheet_name(),
            "timezone": "Africa/Algiers",
            "date_window_start": window_start.isoformat(),
            "date_window_end": window_end.isoformat(),
            "scanned_rows": len(rows),
            "eligible_jobs": len(jobs),
            "skipped_without_links": skipped_without_links,
            "skipped_outside_window": skipped_outside_window,
            "skipped_duplicates": skipped_duplicates,
            "backfilled_from_published_date": backfilled,
            "max_rows": _cv_match_max_rows(),
        },
    }


def _public_cv_match(job: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": _to_text(job.get("id"), default="unknown"),
        "score": int(job.get("score", 0)),
        "source": _to_text(job.get("source"), default="unknown"),
        "title": _to_text(job.get("title"), default="Not specified"),
        "company_name": _to_text(job.get("company_name"), default="Not specified"),
        "location": _to_text(job.get("location"), default="Not specified"),
        "apply_url": _to_text(job.get("apply_url"), default=""),
        "published_date": _to_text(job.get("published_date"), default="Not specified"),
        "published_time_utc": _to_text(job.get("published_time_utc"), default="Not specified"),
        "added_at": _to_text(job.get("added_at"), default=""),
        "arrival_date": _to_text(job.get("arrival_date"), default=""),
        "date_basis": _to_text(job.get("date_basis"), default=""),
        "reasons": [str(reason) for reason in job.get("reasons", []) if str(reason).strip()][:5],
    }


def _job_key(job: dict[str, Any]) -> str:
    job_id = _to_text(job.get("id"))
    if job_id and job_id != "unknown":
        return f"id:{job_id}"

    parts = (
        _to_text(job.get("source")).lower(),
        _to_text(job.get("title")).lower(),
        _to_text(job.get("company_name")).lower(),
        _to_text(job.get("apply_url")).lower(),
    )
    return "|".join(parts)


def _extract_jobs(payload: dict[str, Any]) -> list[dict[str, Any]]:
    jobs = payload.get("jobs", [])
    if not isinstance(jobs, list):
        raise HTTPException(
            status_code=500, detail="Latest digest jobs payload is invalid"
        )
    if not all(isinstance(job, dict) for job in jobs):
        raise HTTPException(
            status_code=500, detail="Latest digest jobs payload is invalid"
        )
    return jobs


def _recent_jobs(primary_payload: dict[str, Any], *, limit: int) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add_from(payload: dict[str, Any]) -> None:
        for job in _extract_jobs(payload):
            key = _job_key(job)
            if key in seen:
                continue
            seen.add(key)
            jobs.append(job)
            if len(jobs) >= limit:
                return

    add_from(primary_payload)
    if len(jobs) >= limit:
        return jobs[:limit]

    history_dir = _digest_history_dir()
    if not history_dir.exists() or not history_dir.is_dir():
        return jobs

    candidates = sorted(
        history_dir.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True
    )
    for path in candidates:
        try:
            payload = _read_latest_digest(path)
        except HTTPException:
            continue
        add_from(payload)
        if len(jobs) >= limit:
            break

    return jobs[:limit]


_load_dotenv_if_available()
app = FastAPI(title="JobStream DZ API", version="0.1.0")

if LANDING_DIR.exists():
    app.mount(
        "/landing", StaticFiles(directory=str(LANDING_DIR), html=True), name="landing"
    )

if JOBS_TODAY_DIR.exists():
    app.mount(
        "/jobs-today",
        StaticFiles(directory=str(JOBS_TODAY_DIR), html=True),
        name="jobs-today",
    )

if CV_MATCH_DIR.exists():
    app.mount(
        "/cv-match",
        StaticFiles(directory=str(CV_MATCH_DIR), html=True),
        name="cv-match",
    )


def _serve_file(path: Path) -> FileResponse:
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {path.name}")
    return FileResponse(path)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    if not LANDING_DIR.exists():
        raise HTTPException(status_code=404, detail="Landing directory not found")
    return RedirectResponse(url="/landing/", status_code=307)


@app.get("/logo.png", include_in_schema=False)
def logo() -> FileResponse:
    return _serve_file(LOGO_FILE)


@app.get("/landing.png", include_in_schema=False)
def landing_reference() -> FileResponse:
    return _serve_file(LANDING_REFERENCE_FILE)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/feed/latest")
def latest_feed() -> dict[str, Any]:
    payload = _read_latest_digest(_latest_digest_path())

    jobs = _recent_jobs(payload, limit=_feed_limit())
    if not jobs:
        raise HTTPException(
            status_code=503,
            detail="Latest digest has no publishable jobs for landing feed",
        )

    return {
        "digest_id": _to_text(payload.get("digest_id"), default="unknown"),
        "published_at": _to_text(payload.get("published_at"), default=""),
        "job_count": len(jobs),
        "jobs": [_public_job(job) for job in jobs],
    }


@app.get("/api/jobs/today")
def jobs_today(days: int = Query(1, ge=1, le=30)) -> dict[str, Any]:
    safe_days = min(days, _today_jobs_max_days())
    return _cached_today_payload(days=safe_days)


@app.get("/api/jobs/recent")
def recent_jobs(
    days: int = Query(7, ge=1, le=7),
    hours: int | None = Query(None, ge=24, le=24),
) -> dict[str, Any]:
    key = ("hours", hours) if hours is not None else ("days", days)
    with _recent_jobs_cache_lock:
        now = time.monotonic()
        clock = datetime.now(ALGERIA_TZ)
        if cached := _recent_jobs_cache.get(key):
            if now < cached[0] and cached[1]["date"] == clock.date().isoformat():
                return _rolling_recent_payload(cached[1], clock) if hours is not None else cached[1]
        payload = _today_payload(days=days, scan_all=True, hours=hours)
        _recent_jobs_cache[key] = (time.monotonic() + 120, payload)
        return _rolling_recent_payload(payload, datetime.now(ALGERIA_TZ)) if hours is not None else payload


@app.post("/api/cv/match")
async def cv_match(request: Request, cv: UploadFile = File(...)) -> dict[str, Any]:
    _enforce_cv_match_rate_limit(request)

    max_bytes = _cv_match_max_file_mb() * 1024 * 1024
    data = await cv.read(max_bytes + 1)
    if not data:
        raise HTTPException(status_code=400, detail="Upload a CV file to find matches.")
    if len(data) > max_bytes:
        raise HTTPException(status_code=400, detail=f"CV file is too large. Maximum size is {_cv_match_max_file_mb()} MB.")

    try:
        cv_text = extract_cv_text(filename=cv.filename or "", data=data)
    except CVParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    jobs_payload = _cv_match_jobs_payload()

    try:
        candidate_profile = extract_candidate_profile(
            cv_text=cv_text,
            api_key=_openai_api_key(),
            model=_cv_match_model(),
            text_char_limit=_cv_match_text_char_limit(),
        )
    except CVProfileError as exc:
        status_code = 500 if "OPENAI_API_KEY" in str(exc) else 502
        raise HTTPException(status_code=status_code, detail="CV profile extraction failed. Please try again later.") from exc

    matches = rank_jobs_for_profile(
        profile=candidate_profile,
        jobs=jobs_payload["jobs"],
        limit=_cv_match_limit(),
    )

    return {
        "candidate_summary": candidate_profile,
        "match_count": len(matches),
        "matches": [_public_cv_match(match) for match in matches],
        "meta": {
            **jobs_payload["meta"],
            "model": _cv_match_model(),
            "match_limit": _cv_match_limit(),
        },
    }
