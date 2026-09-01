"""Normalization helpers shared by source adapters."""

from __future__ import annotations

import hashlib
import html
import math
import re
import unicodedata
from datetime import date, datetime, timezone
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

MISSING = "Not specified"
_TRACKING_PARAMETERS = {"fbclid", "gclid", "trk", "trkinfo"}


def clean_text(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    text = html.unescape(str(value)).replace("\r", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()


def strip_html(value: Any) -> str:
    text = clean_text(value)
    if not text:
        return ""
    text = re.sub(r"<br\s*/?>|</(?:p|li|h[1-6])>", " ", text, flags=re.I)
    return clean_text(re.sub(r"<[^>]+>", "", text))


def labels(items: Any) -> str:
    if not isinstance(items, list):
        return ""
    return " | ".join(
        label
        for item in items
        if isinstance(item, dict) and (label := clean_text(item.get("label")))
    )


def slugify(value: Any) -> str:
    text = unicodedata.normalize("NFKD", clean_text(value)).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def canonical_url(value: Any) -> str:
    raw = clean_text(value)
    if not raw:
        return ""
    parsed = urlsplit(raw)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return ""
    query = urlencode(
        [
            (key, item)
            for key, item in parse_qsl(parsed.query, keep_blank_values=True)
            if not key.lower().startswith("utm_") and key.lower() not in _TRACKING_PARAMETERS
        ]
    )
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, query, ""))


def utc_parts(value: Any) -> tuple[str, str]:
    if value is None or value == "":
        return MISSING, MISSING
    if isinstance(value, date) and not isinstance(value, datetime):
        return value.isoformat(), "00:00:00"
    if isinstance(value, datetime):
        dt = value
    else:
        raw = clean_text(value)
        try:
            number = float(raw)
            if number > 1_000_000_000_000:
                number /= 1000
            dt = datetime.fromtimestamp(number, tz=timezone.utc)
        except (ValueError, TypeError, OSError, OverflowError):
            try:
                dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            except ValueError:
                return MISSING, MISSING
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")


def stable_fallback_id(source: str, values: Iterable[Any]) -> str:
    normalized = "\x1f".join(clean_text(value).casefold() for value in values)
    return hashlib.sha256(f"{source}\x1f{normalized}".encode()).hexdigest()[:24]
