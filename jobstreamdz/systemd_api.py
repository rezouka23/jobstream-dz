from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


def _to_text(value: Any, default: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text or default


def _feed_limit() -> int:
    try:
        return max(1, min(25, int(os.getenv("FEED_LIMIT", "10"))))
    except ValueError:
        return 10


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid JSON object: {path}")
    return payload


def _extract_jobs(payload: dict[str, Any]) -> list[dict[str, Any]]:
    jobs = payload.get("jobs", [])
    if not isinstance(jobs, list) or not all(isinstance(job, dict) for job in jobs):
        raise ValueError("Invalid jobs payload")
    return jobs


def _job_key(job: dict[str, Any]) -> str:
    job_id = _to_text(job.get("id"))
    if job_id and job_id != "unknown":
        return f"id:{job_id}"
    return "|".join(
        _to_text(job.get(name)).lower()
        for name in ("source", "title", "company_name", "apply_url")
    )


def _public_job(job: dict[str, Any]) -> dict[str, str]:
    return {
        "id": _to_text(job.get("id"), "unknown"),
        "source": _to_text(job.get("source"), "unknown"),
        "title": _to_text(job.get("title"), "Not specified"),
        "company_name": _to_text(job.get("company_name"), "Not specified"),
        "location": _to_text(job.get("location"), "Not specified"),
        "apply_url": _to_text(job.get("apply_url")),
        "published_date": _to_text(job.get("published_date"), "Not specified"),
        "published_time_utc": _to_text(job.get("published_time_utc"), "Not specified"),
    }


def latest_feed() -> dict[str, Any]:
    latest_path = Path(os.getenv("LATEST_DIGEST_FILE", "latest_digest.json"))
    history_dir = Path(os.getenv("DIGESTS_DIR", "digest_history"))
    limit = _feed_limit()
    payload = _read_json(latest_path)
    jobs: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add_from(candidate: dict[str, Any]) -> None:
        for job in _extract_jobs(candidate):
            key = _job_key(job)
            if key in seen:
                continue
            seen.add(key)
            jobs.append(job)
            if len(jobs) >= limit:
                return

    add_from(payload)
    if len(jobs) < limit and history_dir.is_dir():
        for path in sorted(history_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                add_from(_read_json(path))
            except Exception:
                continue
            if len(jobs) >= limit:
                break

    if not jobs:
        raise FileNotFoundError("No jobs available")
    return {
        "digest_id": _to_text(payload.get("digest_id"), "unknown"),
        "published_at": _to_text(payload.get("published_at")),
        "job_count": len(jobs),
        "jobs": [_public_job(job) for job in jobs[:limit]],
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "JobStreamAPI/0.1"

    def do_GET(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] == "/healthz":
            self._json(HTTPStatus.OK, {"status": "ok"})
            return
        if self.path.split("?", 1)[0] == "/api/feed/latest":
            try:
                self._json(HTTPStatus.OK, latest_feed())
            except FileNotFoundError as exc:
                self._json(HTTPStatus.NOT_FOUND, {"detail": str(exc)})
            except Exception as exc:
                self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"detail": str(exc)})
            return
        self._json(HTTPStatus.NOT_FOUND, {"detail": "Not found"})

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"{self.address_string()} - {fmt % args}", flush=True)

    def _json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    host = os.getenv("JOBSTREAM_API_HOST", "127.0.0.1")
    port = int(os.getenv("JOBSTREAM_API_PORT", "5001"))
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()