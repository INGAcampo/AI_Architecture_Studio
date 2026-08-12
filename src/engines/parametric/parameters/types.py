from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any


class ParameterType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    ENUM = "enum"
    LENGTH = "length"
    AREA = "area"
    VOLUME = "volume"
    ANGLE = "angle"
    MATERIAL = "material"
    OBJECT_REF = "object_ref"


class ParameterScope(str, Enum):
    INSTANCE = "instance"
    TYPE = "type"
    SHARED = "shared"


class ParameterAccess(str, Enum):
    READ_WRITE = "read_write"
    READ_ONLY = "read_only"
    CALCULATED = "calculated"


@dataclass(frozen=True, slots=True)
class ParameterDefinition:
    parameter_id: str
    name: str
    parameter_type: ParameterType
    group: str = "General"
    scope: ParameterScope = ParameterScope.INSTANCE
    access: ParameterAccess = ParameterAccess.READ_WRITE
    default_value: Any = None
    unit: str | None = None
    minimum: float | None = None
    maximum: float | None = None
    enum_values: tuple[str, ...] = ()
    shared_key: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.parameter_id.strip():
            raise ValueError("parameter_id no puede estar vacío")
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")
        if self.parameter_type is ParameterType.ENUM and not self.enum_values:
            raise ValueError("Los parámetros ENUM requieren enum_values")
        if self.minimum is not None and self.maximum is not None and self.minimum > self.maximum:
            raise ValueError("minimum no puede ser mayor que maximum")
        if self.scope is ParameterScope.SHARED and not (self.shared_key or "").strip():
            raise ValueError("Los parámetros compartidos requieren shared_key")
        for bound in (self.minimum, self.maximum):
            if bound is not None and not isfinite(bound):
                raise ValueError("Los límites deben ser finitos")


@dataclass(slots=True)
class ParameterValue:
    definition: ParameterDefinition
    value: Any
    revision: int = 0
    source: str = "default"
    error: str | None = None

    def snapshot(self) -> dict[str, Any]:
        return {
            "parameter_id": self.definition.parameter_id,
            "value": self.value,
            "revision": self.revision,
            "source": self.source,
            "error": self.error,
        }


@dataclass(frozen=True, slots=True)
class ParameterChange:
    owner_id: str
    parameter_id: str
    old_value: Any
    new_value: Any
    revision: int
    source: str = "user"
