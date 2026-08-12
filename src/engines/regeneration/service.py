from __future__ import annotations

from collections.abc import Callable, Iterable

from .engine import RegenerationEngine
from .model import RegenerationItem


class RegenerationService:
    def __init__(self, engine: RegenerationEngine | None = None) -> None:
        self.engine = engine or RegenerationEngine()

    def register_callback(
        self,
        object_id: str,
        callback: Callable,
        *,
        priority: int = 100,
        dependencies: Iterable[str] = (),
    ) -> RegenerationItem:
        item = RegenerationItem(
            object_id=object_id,
            callback=callback,
            priority=priority,
            dependencies=tuple(dependencies),
        )
        self.engine.register(item)
        return item

    def invalidate(self, object_id: str) -> None:
        self.engine.mark_dirty(object_id)

    def regenerate_all(self):
        return self.engine.regenerate()

    def regenerate_selected(self, object_ids: Iterable[str]):
        return self.engine.regenerate(tuple(object_ids))
