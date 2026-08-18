from __future__ import annotations
from .scene import CadScene

class SelectionManager:
    def __init__(self, scene: CadScene) -> None:
        self.scene = scene
        self._selected: set[str] = set()

    def select(self, entity_id: str, additive: bool = False) -> None:
        self.scene.get(entity_id)
        if not additive:
            self._selected.clear()
        self._selected.add(entity_id)

    def deselect(self, entity_id: str) -> None:
        self._selected.discard(entity_id)

    def clear(self) -> None:
        self._selected.clear()

    def ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._selected))
