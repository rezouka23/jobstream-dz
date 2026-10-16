"""Public job-feed snapshots with nonblocking refresh and restart persistence."""

from __future__ import annotations

import json
import logging
import math
import os
import tempfile
import time
from pathlib import Path
from threading import Event, Lock, Thread
from typing import Any, Callable

LOGGER = logging.getLogger(__name__)


class FeedUnavailable(RuntimeError):
    pass


class PublicFeedCache:
    def __init__(
        self, loader: Callable[[], dict[str, Any]], *,
        snapshot_path: Path | None = None, namespace: str = "",
        ttl: float = 120, max_stale: float = 900,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.loader = loader
        self.snapshot_path = snapshot_path
        self.namespace = namespace
        self.ttl = ttl
        self.max_stale = max_stale
        self.clock = clock
        self._lock = Lock()
        self._refresh_lock = Lock()
        self._stop = Event()
        self._worker: Thread | None = None
        self._scheduled = False
        self._payload: dict[str, Any] | None = None
        self._saved_at = 0.0
        self._retry_at = 0.0
        self._restore()

    @staticmethod
    def _validate(payload: Any) -> None:
        if not isinstance(payload, dict) or not isinstance(payload.get("meta"), dict):
            raise ValueError("Invalid public feed snapshot")
        if not isinstance(payload.get("date"), str) or not isinstance(payload.get("generated_at"), str):
            raise ValueError("Invalid public feed timestamps")
        if not isinstance(payload["meta"].get("skipped_outside_window"), int):
            raise ValueError("Invalid public feed metadata")
        if not isinstance(payload.get("jobs"), list) or not all(
            isinstance(job, dict) and isinstance(job.get("arrival_at"), str)
            for job in payload["jobs"]
        ):
            raise ValueError("Invalid public feed jobs")

    def _restore(self) -> None:
        if self.snapshot_path is None:
            return
        try:
            if self.snapshot_path.stat().st_size > 8 * 1024 * 1024:
                return
            data = json.loads(self.snapshot_path.read_text())
            saved_at = float(data["saved_at"])
            age = self.clock() - saved_at
            if data.get("namespace") != self.namespace or not math.isfinite(saved_at) or not 0 <= age <= self.max_stale:
                return
            self._validate(data["payload"])
            self._payload, self._saved_at = data["payload"], saved_at
        except FileNotFoundError:
            pass
        except (OSError, ValueError, TypeError, KeyError):
            LOGGER.warning("Ignored unusable public feed snapshot")

    def _persist(self, payload: dict[str, Any], saved_at: float) -> None:
        if self.snapshot_path is None:
            return
        temporary: Path | None = None
        try:
            self.snapshot_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.snapshot_path.parent, delete=False) as handle:
                temporary = Path(handle.name)
                json.dump({"namespace": self.namespace, "saved_at": saved_at, "payload": payload}, handle, allow_nan=False)
                handle.flush()
                os.fsync(handle.fileno())
            temporary.replace(self.snapshot_path)
        except (OSError, ValueError, TypeError):
            LOGGER.warning("Could not persist public feed snapshot")
        finally:
            if temporary is not None:
                try:
                    temporary.unlink(missing_ok=True)
                except OSError:
                    pass

    def _usable(self) -> dict[str, Any] | None:
        with self._lock:
            if self._payload is not None and 0 <= self.clock() - self._saved_at <= self.max_stale:
                return self._payload
        return None

    def refresh(self, *, force: bool = False) -> dict[str, Any]:
        with self._refresh_lock:
            with self._lock:
                if not force and self._payload is not None and 0 <= self.clock() - self._saved_at < self.ttl:
                    return self._payload
                if self.clock() < self._retry_at:
                    raise FeedUnavailable("Public feed refresh is cooling down")
            try:
                payload = self.loader()
                self._validate(payload)
            except Exception as exc:
                with self._lock:
                    self._retry_at = self.clock() + 15
                LOGGER.warning("Public feed refresh failed (%s)", type(exc).__name__)
                raise FeedUnavailable("Public job feed is temporarily unavailable") from None
            saved_at = self.clock()
            with self._lock:
                self._payload, self._saved_at = payload, saved_at
                self._retry_at = 0.0
            self._persist(payload, saved_at)
            return payload

    def refresh_background(self) -> None:
        with self._lock:
            if self._scheduled or self.clock() < self._retry_at:
                return
            self._scheduled = True

        def run() -> None:
            try:
                self.refresh()
            except FeedUnavailable:
                pass
            finally:
                with self._lock:
                    self._scheduled = False

        Thread(target=run, name="homepage-feed-refresh", daemon=True).start()

    def get(self) -> dict[str, Any]:
        payload = self._usable()
        if payload is not None:
            with self._lock:
                stale = self.clock() - self._saved_at >= self.ttl
            if stale:
                self.refresh_background()
            return payload
        return self.refresh()

    def start(self) -> None:
        if self._worker is not None and self._worker.is_alive():
            return
        self._stop.clear()

        def run() -> None:
            while not self._stop.is_set():
                delay = self.ttl
                try:
                    self.refresh()
                except FeedUnavailable:
                    delay = 15
                self._stop.wait(delay)

        self._worker = Thread(target=run, name="homepage-feed-warmer", daemon=True)
        self._worker.start()

    def stop(self) -> None:
        self._stop.set()
        if self._worker is not None:
            self._worker.join(timeout=0.2)
