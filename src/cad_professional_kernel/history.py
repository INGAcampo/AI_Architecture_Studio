from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

class Action(Protocol):
    def do(self) -> None: ...
    def undo(self) -> None: ...

class HistoryManager:
    def __init__(self) -> None:
        self._undo: list[Action] = []
        self._redo: list[Action] = []

    def execute(self, action: Action) -> None:
        action.do()
        self._undo.append(action)
        self._redo.clear()

    def undo(self) -> bool:
        if not self._undo:
            return False
        action = self._undo.pop()
        action.undo()
        self._redo.append(action)
        return True

    def redo(self) -> bool:
        if not self._redo:
            return False
        action = self._redo.pop()
        action.do()
        self._undo.append(action)
        return True
