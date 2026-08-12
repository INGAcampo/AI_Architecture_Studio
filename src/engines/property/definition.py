"""Definición inmutable de una propiedad de AIAS."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from .exceptions import PropertyValidationError
from .groups import PropertyGroup
from .types import PropertyType
from .validators import PropertyValidator


@dataclass(frozen=True)
class PropertyDefinition:
    name: str
    property_type: PropertyType | str
    display_name: str | None = None
    group: PropertyGroup | str = PropertyGroup.GENERAL
    unit: str | None = None
    default: Any = None
    required: bool = False
    read_only: bool = False
    visible: bool = True
    description: str = ""
    validators: tuple[PropertyValidator, ...] = field(default_factory=tuple)
    definition_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        name = str(self.name).strip()
        if not name:
            raise ValueError("El nombre de la propiedad no puede estar vacío.")

        object.__setattr__(self, "name", name)
        object.__setattr__(
            self,
            "display_name",
            str(self.display_name or name),
        )
        object.__setattr__(
            self,
            "property_type",
            PropertyType(self.property_type),
        )
        object.__setattr__(
            self,
            "group",
            PropertyGroup.coerce(self.group),
        )
        object.__setattr__(self, "validators", tuple(self.validators))

        if self.default is not None:
            self.validate(self.default)

    def coerce(self, value: Any) -> Any:
        return self.property_type.coerce(value)

    def validate(self, value: Any) -> Any:
        if value is None and self.required:
            raise PropertyValidationError(
                f"La propiedad {self.name!r} es obligatoria."
            )

        converted = self.coerce(value)
        for validator in self.validators:
            validator.validate(converted)
        return converted

    def to_dict(self) -> dict[str, Any]:
        group = self.group.value if isinstance(self.group, PropertyGroup) else self.group
        return {
            "definition_id": self.definition_id,
            "name": self.name,
            "display_name": self.display_name,
            "property_type": self.property_type.value,
            "group": group,
            "unit": self.unit,
            "default": _serialize_scalar(self.default),
            "required": self.required,
            "read_only": self.read_only,
            "visible": self.visible,
            "description": self.description,
        }


def _serialize_scalar(value: Any) -> Any:
    isoformat = getattr(value, "isoformat", None)
    if callable(isoformat):
        return isoformat()
    return value
