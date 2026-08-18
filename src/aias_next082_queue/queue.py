"""In-memory deterministic queue for evidence under review."""
from __future__ import annotations
from typing import Any, Mapping

class IntakeQueue:
    def __init__(self) -> None:
        self._items: list[dict[str, Any]] = []
    def enqueue(self, record: Mapping[str, Any]) -> dict[str, Any]:
        item = dict(record)
        item["queue_status"] = "PENDING_REVIEW"
        item["approved"] = False
        self._items.append(item)
        return item
    def snapshot(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self._items]
