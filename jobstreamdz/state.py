from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class PostedState:
    fingerprints: set[str] = field(default_factory=set)


def load_state(path: Path) -> PostedState:
    if not path.exists():
        return PostedState()

    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, list):
        return PostedState(fingerprints={str(item) for item in payload})

    if isinstance(payload, dict):
        items = payload.get("fingerprints", [])
        if not isinstance(items, list):
            raise ValueError(
                f"Invalid state file format in {path}: fingerprints must be a list"
            )
        return PostedState(fingerprints={str(item) for item in items})

    raise ValueError(f"Invalid state file format in {path}")


def save_state(path: Path, state: PostedState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "fingerprints": sorted(state.fingerprints),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
