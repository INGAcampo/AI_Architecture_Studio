from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .engine import ParameterEngine


@dataclass(slots=True)
class ParameterEditAction:
    engine: ParameterEngine
    owner_id: str
    parameter_id: str
    old_value: Any
    new_value: Any
    label: str = "Editar parámetro"

    def redo(self) -> None:
        self.engine.get_collection(self.owner_id).set(
            self.parameter_id,
            self.new_value,
            source="history.redo",
        )

    def undo(self) -> None:
        self.engine.get_collection(self.owner_id).set(
            self.parameter_id,
            self.old_value,
            source="history.undo",
        )
