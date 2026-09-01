"""Source adapter interface."""

from __future__ import annotations

from typing import Protocol

from ..schema import Job


class SourceAdapter(Protocol):
    name: str

    def fetch(self) -> list[Job]: ...
