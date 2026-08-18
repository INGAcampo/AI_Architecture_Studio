"""Valor enlazado a una definición tipada."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .definition import PropertyDefinition
from .exceptions import PropertyReadOnlyError


@dataclass
class PropertyValue:
    definition: PropertyDefinition
    value: Any = None
    source: str = "instance"
    inherited: bool = False
    calculated: bool = False

    def __post_init__(self) -> None:
        initial = (
            self.definition.default
            if self.value is None
            else self.value
        )
        self.value = self.definition.validate(initial)

    def set(self, value: Any, *, force: bool = False) -> Any:
        if self.definition.read_only and not force:
            raise PropertyReadOnlyError(
                f"La propiedad {self.definition.name!r} es de solo lectura."
            )
        previous = self.value
        self.value = self.definition.validate(value)
        return previous

    def to_dict(self) -> dict[str, Any]:
        return {
            "definition_id": self.definition.definition_id,
            "name": self.definition.name,
            "value": _serialize_scalar(self.value),
            "source": self.source,
            "inherited": self.inherited,
            "calculated": self.calculated,
        }


def _serialize_scalar(value: Any) -> Any:
    isoformat = getattr(value, "isoformat", None)
    if callable(isoformat):
        return isoformat()
    return value
