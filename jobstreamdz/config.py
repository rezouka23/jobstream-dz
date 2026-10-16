from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_SHEET_NAME = "emploitic_jobs_all_algeria_clean"
DEFAULT_REMOTE_SHEET_NAME = "remote"


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    telegram_chat_id: str
    telegram_channel_label: str
    spreadsheet_id: str
    sheet_name: str
    poll_seconds: int
    post_limit: int
    max_rows: int
    state_file: Path
    digests_dir: Path
    latest_digest_file: Path
    remote_enabled: bool
    remote_sheet_name: str
    remote_poll_seconds: int
    remote_post_limit: int
    remote_latest_digest_file: Path
    remote_digests_dir: Path
    remote_require_full_batch: bool
    require_full_batch: bool
    single_run: bool
    google_service_account_file: Path | None
    google_service_account_json: dict[str, Any] | None


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(f"Invalid boolean value for {name}: {value}")


def _env_int(name: str, default: int, minimum: int = 1) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        value = default
    else:
        try:
            value = int(raw.strip())
        except ValueError as exc:
            raise ValueError(f"Invalid integer value for {name}: {raw}") from exc

    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}, got {value}")
    return value


def _load_service_account_json(raw: str) -> dict[str, Any]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON") from exc

    private_key = data.get("private_key")
    if isinstance(private_key, str):
        data["private_key"] = private_key.replace("\\n", "\n")

    return data


def load_settings() -> Settings:
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    spreadsheet_id = os.getenv("SPREADSHEET_ID", "").strip()

    if not telegram_bot_token:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN")
    if not telegram_chat_id:
        raise ValueError("Missing TELEGRAM_CHAT_ID")
    if not spreadsheet_id:
        raise ValueError("Missing SPREADSHEET_ID")

    google_service_account_file_raw = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_FILE", ""
    ).strip()
    google_service_account_json_raw = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_JSON", ""
    ).strip()

    google_service_account_file: Path | None = None
    google_service_account_json: dict[str, Any] | None = None

    if google_service_account_json_raw:
        google_service_account_json = _load_service_account_json(
            google_service_account_json_raw
        )
    elif google_service_account_file_raw:
        candidate = Path(google_service_account_file_raw).expanduser()
        if not candidate.exists():
            raise ValueError(f"GOOGLE_SERVICE_ACCOUNT_FILE does not exist: {candidate}")
        google_service_account_file = candidate
    else:
        raise ValueError(
            "Missing Google credentials: set GOOGLE_SERVICE_ACCOUNT_FILE or GOOGLE_SERVICE_ACCOUNT_JSON"
        )

    return Settings(
        telegram_bot_token=telegram_bot_token,
        telegram_chat_id=telegram_chat_id,
        telegram_channel_label=os.getenv(
            "TELEGRAM_CHANNEL_LABEL", "JobStream DZ"
        ).strip()
        or "JobStream DZ",
        spreadsheet_id=spreadsheet_id,
        sheet_name=os.getenv("SHEET_NAME", DEFAULT_SHEET_NAME).strip()
        or DEFAULT_SHEET_NAME,
        poll_seconds=_env_int("POLL_SECONDS", 300),
        post_limit=_env_int("POST_LIMIT", 5),
        max_rows=_env_int("MAX_ROWS", 250),
        state_file=Path(
            os.getenv("TELEGRAM_STATE_FILE", "seen_telegram_jobs.json")
        ).expanduser(),
        digests_dir=Path(os.getenv("DIGESTS_DIR", "digest_history")).expanduser(),
        latest_digest_file=Path(
            os.getenv("LATEST_DIGEST_FILE", "latest_digest.json")
        ).expanduser(),
        remote_enabled=_env_bool("REMOTE_ENABLED", True),
        remote_sheet_name=os.getenv(
            "REMOTE_SHEET_NAME", DEFAULT_REMOTE_SHEET_NAME
        ).strip()
        or DEFAULT_REMOTE_SHEET_NAME,
        remote_poll_seconds=_env_int("REMOTE_POLL_SECONDS", 900),
        remote_post_limit=_env_int("REMOTE_POST_LIMIT", 5),
        remote_latest_digest_file=Path(
            os.getenv("REMOTE_LATEST_DIGEST_FILE", "latest_remote_digest.json")
        ).expanduser(),
        remote_digests_dir=Path(
            os.getenv("REMOTE_DIGESTS_DIR", "digest_history/remote")
        ).expanduser(),
        remote_require_full_batch=_env_bool("REMOTE_REQUIRE_FULL_BATCH", True),
        require_full_batch=_env_bool("REQUIRE_FULL_BATCH", True),
        single_run=_env_bool("SINGLE_RUN", False),
        google_service_account_file=google_service_account_file,
        google_service_account_json=google_service_account_json,
    )
