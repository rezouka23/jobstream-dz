from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from jobstream import api


ALGERIA_TZ = ZoneInfo("Africa/Algiers")


@pytest.fixture(autouse=True)
def api_state(monkeypatch: pytest.MonkeyPatch) -> None:
    api._rate_limit_hits.clear()
    monkeypatch.setenv("SPREADSHEET_ID", "test-sheet")
    monkeypatch.setenv("SHEET_NAME", "jobs")
    monkeypatch.setenv("CV_MATCH_RATE_LIMIT_REQUESTS", "3")


@pytest.fixture
def client() -> TestClient:
    return TestClient(api.app)


def _today() -> str:
    return datetime.now(ALGERIA_TZ).date().isoformat()


def test_health(client: TestClient) -> None:
    assert client.get("/healthz").json() == {"status": "ok"}


def test_latest_feed_reads_recent_sheet_rows_directly(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    rows = [
        {
            "title": "Backend Engineer",
            "company_name": "Acme",
            "location": "Algiers",
            "apply_url": "https://example.com/jobs/1?utm_source=test",
            "added_at": f"{_today()}T08:00:00+01:00",
        },
        {
            "title": "Duplicate",
            "apply_url": "https://example.com/jobs/1",
            "added_at": _today(),
        },
        {
            "title": "No link",
            "added_at": _today(),
        },
        {
            "title": "Old",
            "apply_url": "https://example.com/jobs/old",
            "published_date": "2000-01-01",
        },
    ]
    monkeypatch.setattr(api, "_fetch_rows", lambda **_: rows)

    payload = client.get("/api/feed/latest").json()

    assert payload["job_count"] == 1
    assert payload["jobs"][0]["title"] == "Backend Engineer"
    assert payload["jobs"][0]["apply_url"] == "https://example.com/jobs/1"
    assert payload["meta"]["skipped_duplicates"] == 1
    assert payload["meta"]["skipped_without_links"] == 1
    assert payload["meta"]["skipped_outside_window"] == 1


def test_jobs_today_uses_published_date_fallback(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        api,
        "_fetch_rows",
        lambda **_: [
            {
                "title": "Designer",
                "job_url": "https://example.com/designer",
                "published_date": _today(),
            }
        ],
    )

    payload = client.get("/api/jobs/today").json()

    assert payload["job_count"] == 1
    assert payload["jobs"][0]["date_basis"] == "published_date"


def test_cv_match_parses_profiles_and_ranks_without_external_calls(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(api, "extract_cv_text", lambda **_: "Python backend developer")
    monkeypatch.setattr(
        api,
        "extract_candidate_profile",
        lambda **_: {
            "target_titles": ["backend developer"],
            "skills": ["python"],
            "languages": [],
            "locations": ["algiers"],
            "experience_years": 2,
            "education": [],
            "industries": [],
            "keywords": [],
        },
    )
    monkeypatch.setattr(
        api,
        "_fetch_rows",
        lambda **_: [
            {
                "title": "Backend Developer",
                "description": "Build Python APIs",
                "location": "Algiers",
                "apply_url": "https://example.com/backend",
                "added_at": _today(),
            }
        ],
    )

    response = client.post(
        "/api/cv/match",
        files={"cv": ("resume.txt", b"resume", "text/plain")},
        headers={"x-forwarded-for": "203.0.113.5"},
    )

    assert response.status_code == 200
    assert response.json()["match_count"] == 1
    assert response.json()["matches"][0]["title"] == "Backend Developer"


def test_cv_match_rate_limit_runs_before_parsing(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CV_MATCH_RATE_LIMIT_REQUESTS", "1")
    parse_calls = 0

    def fake_parse(**_: object) -> str:
        nonlocal parse_calls
        parse_calls += 1
        return "resume"

    monkeypatch.setattr(api, "extract_cv_text", fake_parse)
    headers = {"x-forwarded-for": "198.51.100.10"}
    first = client.post(
        "/api/cv/match", files={"cv": ("resume.txt", b"resume")}, headers=headers
    )
    second = client.post(
        "/api/cv/match", files={"cv": ("resume.txt", b"resume")}, headers=headers
    )

    assert first.status_code == 500
    assert second.status_code == 429
    assert second.headers["retry-after"]
    assert parse_calls == 1
