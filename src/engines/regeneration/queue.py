from __future__ import annotations

import heapq
from itertools import count

from .model import RegenerationItem, RegenerationStatus


class RegenerationQueue:
    def __init__(self) -> None:
        self._heap: list[tuple[int, int, RegenerationItem]] = []
        self._counter = count()
        self._ids: set[str] = set()

    def enqueue(self, item: RegenerationItem) -> bool:
        if item.object_id in self._ids:
            return False
        item.status = RegenerationStatus.QUEUED
        heapq.heappush(
            self._heap,
            (item.priority, next(self._counter), item),
        )
        self._ids.add(item.object_id)
        return True

    def dequeue(self) -> RegenerationItem:
        if not self._heap:
            raise IndexError("La cola está vacía")
        _, _, item = heapq.heappop(self._heap)
        self._ids.remove(item.object_id)
        return item

    def remove(self, object_id: str) -> bool:
        if object_id not in self._ids:
            return False
        self._heap = [
            entry for entry in self._heap
            if entry[2].object_id != object_id
        ]
        heapq.heapify(self._heap)
        self._ids.remove(object_id)
        return True

    def __len__(self) -> int:
        return len(self._heap)

    def ids(self) -> tuple[str, ...]:
        return tuple(entry[2].object_id for entry in sorted(self._heap))
