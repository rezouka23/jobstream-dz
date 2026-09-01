"""Durable local deduplication state."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from threading import RLock
from typing import Iterable


class JsonDedupState:
    def __init__(self, path: Path):
        self.path = path
        self._lock = RLock()

    def load(self) -> set[str]:
        with self._lock:
            if not self.path.exists():
                return set()
            try:
                payload = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"Could not read dedup state at {self.path}") from exc
            if not isinstance(payload, dict) or payload.get("version") != 1:
                raise RuntimeError(f"Unsupported dedup state format at {self.path}")
            keys = payload.get("provider_job_ids")
            if not isinstance(keys, list) or not all(isinstance(item, str) for item in keys):
                raise RuntimeError(f"Invalid dedup state entries at {self.path}")
            return set(keys)

    def add(self, provider_job_ids: Iterable[str]) -> None:
        with self._lock:
            values = self.load()
            values.update(item for item in provider_job_ids if item)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary_name = tempfile.mkstemp(
                prefix=f".{self.path.name}.", dir=self.path.parent, text=True
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as temporary:
                    json.dump(
                        {"version": 1, "provider_job_ids": sorted(values)},
                        temporary,
                        ensure_ascii=True,
                        separators=(",", ":"),
                    )
                    temporary.flush()
                    os.fsync(temporary.fileno())
                os.replace(temporary_name, self.path)
            except BaseException:
                Path(temporary_name).unlink(missing_ok=True)
                raise
