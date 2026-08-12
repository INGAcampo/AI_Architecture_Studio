from __future__ import annotations


class DirtyTracker:
    def __init__(self) -> None:
        self._dirty: set[str] = set()
        self.revision = 0

    def mark_dirty(self, object_id: str) -> None:
        if not object_id.strip():
            raise ValueError("object_id no puede estar vacío")
        if object_id not in self._dirty:
            self._dirty.add(object_id)
            self.revision += 1

    def mark_clean(self, object_id: str) -> bool:
        if object_id not in self._dirty:
            return False
        self._dirty.remove(object_id)
        self.revision += 1
        return True

    def is_dirty(self, object_id: str) -> bool:
        return object_id in self._dirty

    def all(self) -> tuple[str, ...]:
        return tuple(sorted(self._dirty))

    def clear(self) -> None:
        if self._dirty:
            self._dirty.clear()
            self.revision += 1
