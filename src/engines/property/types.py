"""Tipos de datos reconocidos por el Property Engine."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from numbers import Real
from typing import Any

from .exceptions import PropertyValidationError


class PropertyType(str, Enum):
    TEXT = "text"
    INTEGER = "integer"
    DECIMAL = "decimal"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    LENGTH = "length"
    AREA = "area"
    VOLUME = "volume"
    ANGLE = "angle"
    FORCE = "force"
    PRESSURE = "pressure"
    TEMPERATURE = "temperature"
    MATERIAL = "material"
    ENUM = "enum"
    OBJECT = "object"

    @property
    def is_numeric(self) -> bool:
        return self in {
            self.INTEGER,
            self.DECIMAL,
            self.LENGTH,
            self.AREA,
            self.VOLUME,
            self.ANGLE,
            self.FORCE,
            self.PRESSURE,
            self.TEMPERATURE,
        }

    def coerce(self, value: Any) -> Any:
        if value is None:
            return None

        try:
            if self in {self.TEXT, self.MATERIAL, self.ENUM}:
                return str(value)
            if self is self.INTEGER:
                if isinstance(value, bool):
                    raise TypeError
                number = int(value)
                if isinstance(value, Real) and float(value) != number:
                    raise TypeError
                return number
            if self.is_numeric:
                if isinstance(value, bool):
                    raise TypeError
                return float(value)
            if self is self.BOOLEAN:
                if isinstance(value, bool):
                    return value
                if isinstance(value, str):
                    normalized = value.strip().lower()
                    if normalized in {"true", "1", "yes", "sí", "si"}:
                        return True
                    if normalized in {"false", "0", "no"}:
                        return False
                if value in {0, 1}:
                    return bool(value)
                raise TypeError
            if self is self.DATE:
                if isinstance(value, datetime):
                    return value.date()
                if isinstance(value, date):
                    return value
                return date.fromisoformat(str(value))
            if self is self.DATETIME:
                if isinstance(value, datetime):
                    return value
                return datetime.fromisoformat(str(value))
            return value
        except (TypeError, ValueError, OverflowError) as error:
            raise PropertyValidationError(
                f"No se puede convertir {value!r} al tipo {self.value!r}."
            ) from error
