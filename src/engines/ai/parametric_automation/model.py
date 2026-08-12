from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable


class ParameterType(str, Enum):
    NUMBER = "number"
    LENGTH = "length"
    AREA = "area"
    VOLUME = "volume"
    ANGLE = "angle"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    TEXT = "text"


@dataclass(frozen=True, slots=True)
class ParameterDefinition:
    parameter_id: str
    parameter_type: ParameterType
    default: Any = None
    minimum: float | None = None
    maximum: float | None = None
    read_only: bool = False

    def __post_init__(self) -> None:
        if not self.parameter_id.strip():
            raise ValueError("parameter_id es obligatorio")
        if self.minimum is not None and self.maximum is not None:
            if self.minimum > self.maximum:
                raise ValueError("minimum no puede ser mayor que maximum")


@dataclass(slots=True)
class ParameterValue:
    definition: ParameterDefinition
    value: Any
    revision: int = 0
    source: str = "default"

    def validate(self, value: Any) -> Any:
        parameter_type = self.definition.parameter_type

        if parameter_type in {
            ParameterType.NUMBER,
            ParameterType.LENGTH,
            ParameterType.AREA,
            ParameterType.VOLUME,
            ParameterType.ANGLE,
        }:
            value = float(value)
        elif parameter_type is ParameterType.INTEGER:
            value = int(value)
        elif parameter_type is ParameterType.BOOLEAN:
            value = bool(value)
        elif parameter_type is ParameterType.TEXT:
            value = str(value)

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if self.definition.minimum is not None and value < self.definition.minimum:
                raise ValueError(
                    f"{self.definition.parameter_id} menor que el mínimo"
                )
            if self.definition.maximum is not None and value > self.definition.maximum:
                raise ValueError(
                    f"{self.definition.parameter_id} mayor que el máximo"
                )

        return value

    def set(self, value: Any, *, source: str = "manual") -> bool:
        if self.definition.read_only and source != "formula":
            raise PermissionError(
                f"Parámetro de solo lectura: {self.definition.parameter_id}"
            )
        normalized = self.validate(value)
        if normalized == self.value:
            return False
        self.value = normalized
        self.revision += 1
        self.source = source
        return True


class ParameterSet:
    def __init__(self, owner_id: str) -> None:
        if not owner_id.strip():
            raise ValueError("owner_id es obligatorio")
        self.owner_id = owner_id
        self._values: dict[str, ParameterValue] = {}
        self.revision = 0

    def define(self, definition: ParameterDefinition) -> ParameterValue:
        if definition.parameter_id in self._values:
            raise ValueError(f"Parámetro duplicado: {definition.parameter_id}")
        value = ParameterValue(
            definition=definition,
            value=ParameterValue(definition, definition.default).validate(
                definition.default
            ),
        )
        self._values[definition.parameter_id] = value
        return value

    def set(self, parameter_id: str, value: Any, *, source: str = "manual") -> bool:
        parameter = self._values[parameter_id]
        changed = parameter.set(value, source=source)
        if changed:
            self.revision += 1
        return changed

    def get(self, parameter_id: str) -> Any:
        return self._values[parameter_id].value

    def item(self, parameter_id: str) -> ParameterValue:
        return self._values[parameter_id]

    def values(self) -> dict[str, Any]:
        return {
            parameter_id: parameter.value
            for parameter_id, parameter in self._values.items()
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "owner_id": self.owner_id,
            "revision": self.revision,
            "values": {
                parameter_id: {
                    "value": parameter.value,
                    "revision": parameter.revision,
                    "source": parameter.source,
                    "type": parameter.definition.parameter_type.value,
                }
                for parameter_id, parameter in self._values.items()
            },
        }

    def __contains__(self, parameter_id: str) -> bool:
        return parameter_id in self._values

    def __iter__(self) -> Iterable[ParameterValue]:
        return iter(self._values.values())
