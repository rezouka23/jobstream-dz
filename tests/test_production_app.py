"""Smoke tests for the backend synchronized from the production server."""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from jobstreamdz import api


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    api._recent_jobs_cache.clear()
    api._today_jobs_cache.clear()
    api._cv_match_rate_limit_hits.clear()
    monkeypatch.setenv("SPREADSHEET_ID", "test-sheet")
    monkeypatch.setenv("SHEET_NAME", "jobs")
    monkeypatch.setenv("CV_MATCH_RATE_LIMIT_REQUESTS", "3")
    monkeypatch.setattr(api, "_create_jobs_sheet_service", lambda **_: object())
    monkeypatch.setattr(api, "_homepage_feed_cache", api.PublicFeedCache(api._load_homepage_feed))
    return TestClient(api.app)


def test_production_pages_and_health_are_available(client: TestClient) -> None:
    assert client.get("/healthz").json() == {"status": "ok"}
    assert client.get("/", follow_redirects=False).headers["location"] == "/landing/"
    for path in ("/landing/", "/jobs-today/", "/cv-match/", "/logo.png"):
        assert client.get(path).status_code == 200


def test_production_recent_search_scans_and_caches_full_window(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    today = datetime.now(api.ALGERIA_TZ).date()
    boundary = (today - timedelta(days=6)).isoformat()
    rows = [
        {
            "title": f"Role {i}",
            "job_url": f"https://example.com/job/{i}",
            "added_at": today.isoformat(),
            "work_mode": "Remote",
        }
        for i in range(1200)
    ] + [
        {"title": "Boundary", "job_url": "https://example.com/boundary", "added_at": boundary},
        {"title": "Too old", "job_url": "https://example.com/old", "added_at": (today - timedelta(days=7)).isoformat()},
    ]
    calls = []

    def fetch(**kwargs):
        calls.append(kwargs)
        return rows

    monkeypatch.setattr(api, "_jobs_sheet_service", lambda: object())
    monkeypatch.setattr(api, "fetch_sheet_rows", fetch)
    response = client.get("/api/jobs/recent?days=7")
    assert response.status_code == 200
    payload = response.json()
    assert payload["job_count"] == 1201
    assert payload["meta"]["date_window_start"] == boundary
    assert payload["jobs"][0]["work_mode"] == "Remote"
    assert calls[0]["max_rows"] is None
    assert client.get("/api/jobs/recent?days=7").json() == payload
    assert len(calls) == 1
    assert client.get("/api/jobs/recent?days=8").status_code == 422


def test_production_cv_rejects_empty_upload_before_external_calls(client: TestClient) -> None:
    response = client.post("/api/cv/match", files={"cv": ("resume.txt", b"", "text/plain")})
    assert response.status_code == 400
    assert "Upload a CV" in response.json()["detail"]


def test_homepage_24_hours_is_rolling_and_today_keeps_calendar_days(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    real_datetime = datetime
    clock = {"now": real_datetime(2026, 10, 16, 1, 0, tzinfo=api.ALGERIA_TZ)}

    class FrozenDatetime(real_datetime):
        @classmethod
        def now(cls, tz=None):
            value = clock["now"]
            return value.astimezone(tz) if tz else value.replace(tzinfo=None)

    monkeypatch.setattr(api, "datetime", FrozenDatetime)
    rows = [
        {"title": title, "job_url": f"https://example.com/{title}", "added_at": (clock["now"] - age).isoformat()}
        for title, age in (
            ("today", timedelta(minutes=30)),
            ("yesterday-evening", timedelta(hours=2)),
            ("boundary", timedelta(hours=24)),
            ("too-old", timedelta(hours=25)),
            ("future", -timedelta(days=1)),
        )
    ]
    calls = []

    def fetch(**kwargs):
        calls.append(kwargs)
        return rows

    monkeypatch.setattr(api, "_jobs_sheet_service", lambda: object())
    monkeypatch.setattr(api, "fetch_sheet_rows", fetch)
    today = client.get("/api/jobs/today").json()
    assert [job["title"] for job in today["jobs"]] == ["today"]

    response = client.get("/api/jobs/recent?hours=24")
    assert response.status_code == 200
    payload = response.json()
    assert [job["title"] for job in payload["jobs"]] == ["today", "yesterday-evening", "boundary"]
    assert payload["meta"]["hours"] == 24
    assert payload["meta"]["window_type"] == "rolling"
    assert all("arrival_at" in job for job in payload["jobs"])
    assert calls[-1]["max_rows"] is None

    # The rolling cutoff must still advance while the underlying sheet is cached.
    clock["now"] += timedelta(seconds=2)
    cached = client.get("/api/jobs/recent?hours=24").json()
    assert [job["title"] for job in cached["jobs"]] == ["today", "yesterday-evening"]
    assert len(calls) == 2
    assert client.get("/api/jobs/today").json() == today
    assert client.get("/api/jobs/recent?hours=25").status_code == 422


def test_homepage_24_hour_timestamp_fallbacks() -> None:
    stamp, basis = api._row_arrival_timestamp({
        "added_at": "Not specified", "scraped_at": "2026-10-15T23:30:00Z",
    })
    assert stamp.isoformat() == "2026-10-16T00:30:00+01:00"
    assert basis == "scraped_at"
    stamp, basis = api._row_arrival_timestamp({
        "published_date": "2026-10-15", "published_time_utc": "23:30 UTC",
    })
    assert stamp.isoformat() == "2026-10-16T00:30:00+01:00"
    assert basis == "published_date"
    stamp, _ = api._row_arrival_timestamp({"published_date": "16/10/2026"})
    assert stamp.isoformat() == "2026-10-16T00:00:00+01:00"
