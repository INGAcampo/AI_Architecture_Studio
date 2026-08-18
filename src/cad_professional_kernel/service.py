from __future__ import annotations
from .commands import AddEntityAction, DeleteEntityAction
from .history import HistoryManager
from .scene import CadScene
from .selection import SelectionManager

class CadKernelService:
    def __init__(self) -> None:
        self.scene = CadScene()
        self.history = HistoryManager()
        self.selection = SelectionManager(self.scene)

    def add(self, entity) -> str:
        self.history.execute(AddEntityAction(self.scene, entity))
        return entity.entity_id

    def delete(self, entity_id: str) -> None:
        self.history.execute(DeleteEntityAction(self.scene, entity_id))
        self.selection.deselect(entity_id)

    def undo(self) -> bool:
        return self.history.undo()

    def redo(self) -> bool:
        return self.history.redo()
