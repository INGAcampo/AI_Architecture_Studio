from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .adapter import _read, _write


@dataclass(slots=True)
class PropertyEditAction:
    targets: tuple[Any, ...]
    property_id: str
    old_values: tuple[Any, ...]
    new_value: Any
    label: str = "Editar propiedad"

    def redo(self) -> None:
        for target in self.targets:
            _write(target, self.property_id, self.new_value)

    def undo(self) -> None:
        for target, old_value in zip(self.targets, self.old_values):
            _write(target, self.property_id, old_value)

    @classmethod
    def create(
        cls,
        targets: Iterable[Any],
        property_id: str,
        new_value: Any,
        *,
        label: str | None = None,
    ) -> "PropertyEditAction":
        target_tuple = tuple(targets)
        return cls(
            targets=target_tuple,
            property_id=property_id,
            old_values=tuple(
                _read(target, property_id) for target in target_tuple
            ),
            new_value=new_value,
            label=label or f"Editar {property_id}",
        )
