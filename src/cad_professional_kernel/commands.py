from __future__ import annotations
from dataclasses import dataclass
from .entities import CadEntity
from .scene import CadScene

@dataclass(slots=True)
class AddEntityAction:
    scene: CadScene
    entity: CadEntity

    def do(self) -> None:
        if self.entity.entity_id not in {e.entity_id for e in self.scene.all()}:
            self.scene.add(self.entity)

    def undo(self) -> None:
        self.scene.remove(self.entity.entity_id)

@dataclass(slots=True)
class DeleteEntityAction:
    scene: CadScene
    entity_id: str
    _entity: CadEntity | None = None

    def do(self) -> None:
        self._entity = self.scene.remove(self.entity_id)

    def undo(self) -> None:
        if self._entity is None:
            raise RuntimeError("Nothing to restore.")
        self.scene.add(self._entity)
