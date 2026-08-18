from __future__ import annotations

from typing import Any

from .types import ParameterAccess, ParameterDefinition, ParameterType
from .units import UnitRegistry


class ParameterValidator:
    def __init__(self, units: UnitRegistry | None = None) -> None:
        self.units = units or UnitRegistry()

    def normalize(self, definition: ParameterDefinition, value: Any) -> Any:
        kind = definition.parameter_type

        if definition.access is ParameterAccess.CALCULATED:
            return value

        if kind in {ParameterType.STRING, ParameterType.MATERIAL, ParameterType.OBJECT_REF}:
            normalized = "" if value is None else str(value)
        elif kind is ParameterType.BOOLEAN:
            normalized = self._boolean(value)
        elif kind is ParameterType.INTEGER:
            if isinstance(value, bool):
                raise ValueError("Un booleano no es un entero válido")
            normalized = int(value)
        elif kind in {
            ParameterType.FLOAT,
            ParameterType.LENGTH,
            ParameterType.AREA,
            ParameterType.VOLUME,
            ParameterType.ANGLE,
        }:
            if isinstance(value, bool):
                raise ValueError("Un booleano no es un número válido")
            normalized = float(value)
        elif kind is ParameterType.ENUM:
            normalized = str(value)
        else:
            normalized = value

        self.validate(definition, normalized)
        return normalized

    def validate(self, definition: ParameterDefinition, value: Any) -> None:
        if definition.parameter_type is ParameterType.ENUM and value not in definition.enum_values:
            raise ValueError(f"Valor no permitido: {value}")

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if definition.minimum is not None and value < definition.minimum:
                raise ValueError(f"{definition.parameter_id} debe ser >= {definition.minimum}")
            if definition.maximum is not None and value > definition.maximum:
                raise ValueError(f"{definition.parameter_id} debe ser <= {definition.maximum}")

        if definition.unit is not None:
            self.units.get(definition.unit)

    @staticmethod
    def _boolean(value: Any) -> bool:
        if isinstance(value, str):
            normalized = value.strip().casefold()
            if normalized in {"true", "1", "yes", "si", "sí"}:
                return True
            if normalized in {"false", "0", "no"}:
                return False
            raise ValueError(f"Valor booleano no válido: {value}")
        return bool(value)
