from __future__ import annotations

import html
import time
from typing import Any

import requests

from .sheets import extract_apply_url


class TelegramSendError(RuntimeError):
    pass


def _text_or_default(value: str, default: str = "Not specified") -> str:
    text = str(value).strip() if value is not None else ""
    return text or default


def _published_label(job: dict[str, str]) -> str:
    published_date = _text_or_default(job.get("published_date", ""))
    published_time = _text_or_default(job.get("published_time_utc", ""))

    has_date = published_date != "Not specified"
    has_time = published_time != "Not specified"

    if has_date and has_time:
        return f"{published_date} {published_time} UTC"
    if has_date:
        return published_date
    if has_time:
        return f"{published_time} UTC"
    return "Not specified"


def _build_main_digest_message(jobs: list[dict[str, str]], channel_label: str) -> str:
    escaped_channel = html.escape(channel_label)
    lines = [
        f"🚀 <b>{escaped_channel} — Fresh Jobs</b>",
        "",
        "✨ New batch just dropped:",
        "",
    ]

    for index, job in enumerate(jobs, start=1):
        title = html.escape(_text_or_default(job.get("title", "")))
        company = html.escape(_text_or_default(job.get("company_name", "")))
        location = html.escape(_text_or_default(job.get("location", "")))
        published = html.escape(_published_label(job))

        apply_url = extract_apply_url(job)
        safe_apply_url = html.escape(apply_url, quote=True)

        lines.append(f"<b>{index}) 💼 {title}</b>")
        lines.append(f"🏢 {company} | 📍 {location}")
        lines.append(f"🕒 {published}")
        if apply_url:
            lines.append(f'🔗 <a href="{safe_apply_url}">Apply now</a>')
        else:
            lines.append("🔗 Link unavailable")
        lines.append("")

    lines.append("#JobStreamDZ #AlgeriaJobs")
    return "\n".join(lines).strip()


def _build_remote_digest_message(jobs: list[dict[str, str]]) -> str:
    lines = [
        "🏠 <b>Télétravail: nouvelles opportunités</b>",
        "",
        "<i>Remote & flexible roles (posted every 15 minutes)</i>",
        "",
    ]

    for job in jobs:
        title = html.escape(_text_or_default(job.get("title", "")))
        company = html.escape(_text_or_default(job.get("company_name", "")))
        location = html.escape(_text_or_default(job.get("location", "")))

        apply_url = extract_apply_url(job)
        safe_apply_url = html.escape(apply_url, quote=True)

        lines.append("🌍 <b>Remote or 🏠 Télétravail</b>")
        lines.append(f"💼 {title}")
        lines.append(f"🏢 {company}")
        lines.append(f"📍 {location}")
        if apply_url:
            lines.append(f'🔗 <a href="{safe_apply_url}">Apply now</a>')
        else:
            lines.append("🔗 Link unavailable")
        lines.append("")

    lines.append("#JobStreamDZ #RemoteJobs")
    return "\n".join(lines).strip()


def build_digest_message(
    jobs: list[dict[str, str]], channel_label: str, *, feed_name: str = "main"
) -> str:
    if feed_name == "remote":
        return _build_remote_digest_message(jobs)

    return _build_main_digest_message(jobs, channel_label)


def send_telegram_message(
    *,
    bot_token: str,
    chat_id: str,
    text: str,
    max_retries: int = 3,
) -> dict[str, Any]:
    endpoint = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(endpoint, json=payload, timeout=30)
        except requests.RequestException as exc:
            if attempt == max_retries:
                raise TelegramSendError(f"Telegram request failed: {exc}") from exc
            time.sleep(min(2**attempt, 15))
            continue

        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                return data
            description = data.get("description", "Unknown Telegram API error")
            if attempt == max_retries:
                raise TelegramSendError(description)
            time.sleep(min(2**attempt, 15))
            continue

        if response.status_code == 429:
            retry_after = 5
            try:
                retry_after = int(
                    response.json().get("parameters", {}).get("retry_after", 5)
                )
            except Exception:
                retry_after = 5
            time.sleep(max(1, retry_after))
            continue

        if 500 <= response.status_code < 600 and attempt < max_retries:
            time.sleep(min(2**attempt, 15))
            continue

        raise TelegramSendError(
            f"Telegram API error {response.status_code}: {response.text.strip() or 'empty response'}"
        )

    raise TelegramSendError("Telegram send failed after retries")
