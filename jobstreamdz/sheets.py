from __future__ import annotations

import html
import hashlib
import re
from typing import Any
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

_UNAVAILABLE_MARKERS = {
    "",
    "link unavailable",
    "lien indisponible",
    "not specified",
    "non specifie",
    "n/a",
    "na",
    "none",
    "null",
    "-",
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


def build_sheets_service(
    *,
    service_account_file: str | None,
    service_account_json: dict[str, Any] | None,
) -> Any:
    if service_account_json is not None:
        credentials = Credentials.from_service_account_info(
            service_account_json, scopes=SCOPES
        )
    elif service_account_file:
        credentials = Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES
        )
    else:
        raise ValueError("Missing Google service account credentials")

    return build("sheets", "v4", credentials=credentials, cache_discovery=False)


def _normalize_header(value: str) -> str:
    return "_".join(value.strip().lower().split())


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def fetch_sheet_rows(
    service: Any, spreadsheet_id: str, sheet_name: str, max_rows: int | None, end_col: str = "Q"
) -> list[dict[str, str]]:
    target_range = f"{sheet_name}!A1:{end_col}{max_rows or ''}"
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

    headers = [_normalize_header(_to_text(item)) for item in values[0]]

    rows: list[dict[str, str]] = []
    for row in values[1:]:
        row_map: dict[str, str] = {}
        for index, header in enumerate(headers):
            if not header:
                continue
            row_map[header] = _to_text(row[index]) if index < len(row) else ""

        if not any(row_map.values()):
            continue
        rows.append(row_map)

    return rows


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _is_unavailable_marker(value: str) -> bool:
    return _normalize_text(value) in _UNAVAILABLE_MARKERS


def _clean_url_token(value: str) -> str:
    cleaned = html.unescape(_to_text(value))
    cleaned = cleaned.strip().strip("\"'`")

    while cleaned and cleaned[-1] in ".,;:!?)]}":
        cleaned = cleaned[:-1]
    while cleaned and cleaned[0] in "([{'\"":
        cleaned = cleaned[1:]

    if cleaned.lower().startswith("www."):
        cleaned = f"https://{cleaned}"

    return cleaned.strip()


def _extract_candidate_urls(text: str) -> list[str]:
    normalized = html.unescape(_to_text(text))
    if not normalized:
        return []

    candidates: list[str] = []
    direct = _clean_url_token(normalized)
    if direct:
        candidates.append(direct)

    for match in _URL_PATTERN.findall(normalized):
        candidate = _clean_url_token(match)
        if candidate:
            candidates.append(candidate)

    unique: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = candidate.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)

    return unique


def _strip_tracking_query(url: str) -> str:
    parts = urlsplit(url)
    if not parts.query:
        return url

    filtered = []
    for key, value in parse_qsl(parts.query, keep_blank_values=False):
        lowered = key.lower()
        if lowered.startswith("utm_"):
            continue
        if lowered in _TRACKING_QUERY_KEYS:
            continue
        filtered.append((key, value))

    query = urlencode(filtered, doseq=True)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, query, ""))


def _unwrap_wrapped_url(url: str) -> str:
    current = url
    seen: set[str] = set()

    for _ in range(3):
        key = current.lower()
        if key in seen:
            break
        seen.add(key)

        parts = urlsplit(current)
        if not parts.query:
            break

        unwrapped = ""
        for query_key, query_value in parse_qsl(parts.query, keep_blank_values=False):
            if query_key.lower() not in _WRAPPED_URL_QUERY_KEYS:
                continue

            decoded = _to_text(query_value)
            for _ in range(2):
                next_decoded = unquote(decoded)
                if next_decoded == decoded:
                    break
                decoded = next_decoded

            candidates = _extract_candidate_urls(decoded)
            if candidates:
                unwrapped = candidates[0]
                break

        if not unwrapped:
            break

        normalized = normalize_url(unwrapped)
        if not normalized:
            break

        current = normalized

    return current


def normalize_url(url: str) -> str:
    raw = _clean_url_token(url)
    if not raw:
        return ""

    parts = urlsplit(raw)
    if parts.scheme and parts.scheme.lower() not in {"http", "https"}:
        return ""
    if not parts.netloc:
        return ""

    scheme = (parts.scheme or "https").lower()
    netloc = parts.netloc.lower()
    path = parts.path.rstrip("/")
    query = parts.query

    normalized = urlunsplit((scheme, netloc, path, query, ""))
    normalized = _strip_tracking_query(normalized)
    return normalized


def extract_apply_url(job: dict[str, str]) -> str:
    fields = [
        _to_text(job.get("apply_url", "")),
        _to_text(job.get("job_url", "")),
    ]

    for field in fields:
        if not field or _is_unavailable_marker(field):
            continue

        for candidate in _extract_candidate_urls(field):
            normalized = normalize_url(candidate)
            if not normalized:
                continue

            unwrapped = _unwrap_wrapped_url(normalized)
            final_url = normalize_url(unwrapped) if unwrapped else normalized
            if final_url:
                return final_url

    return ""


def has_usable_apply_url(job: dict[str, str]) -> bool:
    return bool(extract_apply_url(job))


def fingerprint_job(job: dict[str, str]) -> str:
    apply_url = extract_apply_url(job)
    if apply_url:
        key = apply_url
        return "url:" + hashlib.sha1(key.encode("utf-8")).hexdigest()

    fallback_fields = [
        _normalize_text(_to_text(job.get("source", ""))),
        _normalize_text(_to_text(job.get("title", ""))),
        _normalize_text(_to_text(job.get("company_name", ""))),
        _normalize_text(_to_text(job.get("location", ""))),
    ]
    fallback_key = "|".join(fallback_fields)
    return "fallback:" + hashlib.sha1(fallback_key.encode("utf-8")).hexdigest()
