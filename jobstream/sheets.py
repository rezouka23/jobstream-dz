from __future__ import annotations

import hashlib
import html
import json
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit


SCOPES = ("https://www.googleapis.com/auth/spreadsheets.readonly",)

_UNAVAILABLE_MARKERS = {
    "",
    "-",
    "link unavailable",
    "lien indisponible",
    "n/a",
    "na",
    "non specifie",
    "none",
    "not specified",
    "null",
}
_URL_PATTERN = re.compile(
    r"(https?://[^\s<>'\"\]\[{}]+|www\.[^\s<>'\"\]\[{}]+)", re.IGNORECASE
)
_TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "igshid",
    "mc_cid",
    "mc_eid",
    "mkt_tok",
    "msclkid",
    "si",
    "spm",
    "yclid",
}
_WRAPPED_URL_QUERY_KEYS = (
    "url",
    "u",
    "target",
    "dest",
    "destination",
    "redirect",
    "redirect_url",
    "redir",
    "r",
    "to",
    "next",
    "continue",
    "out",
)


def _to_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _normalize_text(value: Any) -> str:
    return " ".join(_to_text(value).lower().split())


def _service_account_json(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON is invalid JSON") from exc
    if not isinstance(value, dict):
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON must contain an object")

    private_key = value.get("private_key")
    if isinstance(private_key, str):
        value["private_key"] = private_key.replace("\\n", "\n")
    return value


def build_sheets_service(
    *,
    service_account_file: str | None = None,
    service_account_json: Mapping[str, Any] | None = None,
) -> Any:
    """Build a read-only Google Sheets service without loading project secrets."""
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
    except ImportError as exc:  # pragma: no cover - deployment dependency failure
        raise RuntimeError("Google Sheets dependencies are not installed") from exc

    if service_account_json is not None:
        credentials = Credentials.from_service_account_info(
            dict(service_account_json), scopes=SCOPES
        )
    elif service_account_file:
        credentials = Credentials.from_service_account_file(
            str(Path(service_account_file).expanduser()), scopes=SCOPES
        )
    else:
        raise ValueError("Google Sheets credentials are not configured")

    return build("sheets", "v4", credentials=credentials, cache_discovery=False)


@lru_cache(maxsize=1)
def get_sheets_service() -> Any:
    """Build and cache a service from environment-only credentials."""
    raw_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "").strip()
    if raw_json:
        return build_sheets_service(service_account_json=_service_account_json(raw_json))
    if account_file:
        return build_sheets_service(service_account_file=account_file)
    raise ValueError("Google Sheets credentials are not configured")


def fetch_sheet_rows(
    service: Any,
    spreadsheet_id: str,
    sheet_name: str,
    max_rows: int,
    end_col: str = "Z",
) -> list[dict[str, str]]:
    """Read a sheet range and map normalized headers to string cell values."""
    target_range = f"{sheet_name}!A1:{end_col}{max_rows}"
    response = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=target_range,
            valueRenderOption="FORMATTED_VALUE",
        )
        .execute()
    )
    values = response.get("values", [])
    if not values:
        return []

    headers = ["_".join(_to_text(item).lower().split()) for item in values[0]]
    rows: list[dict[str, str]] = []
    for row in values[1:]:
        mapped = {
            header: _to_text(row[index]) if index < len(row) else ""
            for index, header in enumerate(headers)
            if header
        }
        if any(mapped.values()):
            rows.append(mapped)
    return rows


def _clean_url_token(value: Any) -> str:
    cleaned = html.unescape(_to_text(value)).strip().strip("\"'`")
    while cleaned and cleaned[-1] in ".,;:!?)]}":
        cleaned = cleaned[:-1]
    while cleaned and cleaned[0] in "([{'\"":
        cleaned = cleaned[1:]
    if cleaned.lower().startswith("www."):
        cleaned = f"https://{cleaned}"
    return cleaned.strip()


def _extract_candidate_urls(value: Any) -> list[str]:
    text = html.unescape(_to_text(value))
    candidates = [_clean_url_token(text)] if text else []
    candidates.extend(_clean_url_token(match) for match in _URL_PATTERN.findall(text))
    unique: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = candidate.lower()
        if candidate and key not in seen:
            seen.add(key)
            unique.append(candidate)
    return unique


def normalize_url(value: Any) -> str:
    raw = _clean_url_token(value)
    if not raw:
        return ""
    parts = urlsplit(raw)
    if parts.scheme.lower() not in {"http", "https"} or not parts.netloc:
        return ""

    query = [
        (key, item)
        for key, item in parse_qsl(parts.query, keep_blank_values=False)
        if not key.lower().startswith("utm_")
        and key.lower() not in _TRACKING_QUERY_KEYS
    ]
    return urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path.rstrip("/"),
            urlencode(query, doseq=True),
            "",
        )
    )


def _unwrap_url(url: str) -> str:
    current = url
    seen: set[str] = set()
    for _ in range(3):
        if current.lower() in seen:
            break
        seen.add(current.lower())
        parts = urlsplit(current)
        wrapped = ""
        for key, value in parse_qsl(parts.query, keep_blank_values=False):
            if key.lower() not in _WRAPPED_URL_QUERY_KEYS:
                continue
            decoded = unquote(unquote(value))
            candidates = _extract_candidate_urls(decoded)
            if candidates:
                wrapped = normalize_url(candidates[0])
                break
        if not wrapped:
            break
        current = wrapped
    return current


def extract_apply_url(job: Mapping[str, Any]) -> str:
    for field in (job.get("apply_url"), job.get("job_url")):
        if _normalize_text(field) in _UNAVAILABLE_MARKERS:
            continue
        for candidate in _extract_candidate_urls(field):
            normalized = normalize_url(candidate)
            if normalized:
                return normalize_url(_unwrap_url(normalized))
    return ""


def has_usable_apply_url(job: Mapping[str, Any]) -> bool:
    return bool(extract_apply_url(job))


def fingerprint_job(job: Mapping[str, Any]) -> str:
    apply_url = extract_apply_url(job)
    if apply_url:
        return "url:" + hashlib.sha1(apply_url.encode("utf-8")).hexdigest()
    fallback = "|".join(
        _normalize_text(job.get(field))
        for field in ("source", "title", "company_name", "location")
    )
    return "fallback:" + hashlib.sha1(fallback.encode("utf-8")).hexdigest()
