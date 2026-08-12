"""Validadores reutilizables para definiciones de propiedades."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .exceptions import PropertyValidationError


class PropertyValidator(Protocol):
    def validate(self, value: Any) -> None:
        ...


@dataclass(frozen=True)
class RequiredValidator:
    allow_blank: bool = False

    def validate(self, value: Any) -> None:
        if value is None:
            raise PropertyValidationError("El valor es obligatorio.")
        if (
            not self.allow_blank
            and isinstance(value, str)
            and not value.strip()
        ):
            raise PropertyValidationError("El texto no puede estar vacío.")


@dataclass(frozen=True)
class RangeValidator:
    minimum: float | None = None
    maximum: float | None = None
    include_minimum: bool = True
    include_maximum: bool = True

    def validate(self, value: Any) -> None:
        if value is None:
            return
        number = float(value)
        if self.minimum is not None:
            invalid = (
                number < self.minimum
                if self.include_minimum
                else number <= self.minimum
            )
            if invalid:
                raise PropertyValidationError(
                    f"El valor debe ser mayor que "
                    f"{'o igual a ' if self.include_minimum else ''}"
                    f"{self.minimum}."
                )
        if self.maximum is not None:
            invalid = (
                number > self.maximum
                if self.include_maximum
                else number >= self.maximum
            )
            if invalid:
                raise PropertyValidationError(
                    f"El valor debe ser menor que "
                    f"{'o igual a ' if self.include_maximum else ''}"
                    f"{self.maximum}."
                )


@dataclass(frozen=True)
class AllowedValuesValidator:
    values: tuple[Any, ...]
    case_sensitive: bool = True

    def __init__(self, values, case_sensitive: bool = True):
        object.__setattr__(self, "values", tuple(values))
        object.__setattr__(self, "case_sensitive", case_sensitive)

    def validate(self, value: Any) -> None:
        if value is None:
            return
        if self.case_sensitive or not isinstance(value, str):
            valid = value in self.values
        else:
            allowed = {
                str(item).casefold()
                for item in self.values
            }
            valid = value.casefold() in allowed
        if not valid:
            raise PropertyValidationError(
                f"El valor {value!r} no pertenece a los valores permitidos."
            )


@dataclass(frozen=True)
class LengthValidator:
    minimum: int | None = None
    maximum: int | None = None

    def validate(self, value: Any) -> None:
        if value is None:
            return
        size = len(value)
        if self.minimum is not None and size < self.minimum:
            raise PropertyValidationError(
                f"El valor requiere al menos {self.minimum} caracteres."
            )
        if self.maximum is not None and size > self.maximum:
            raise PropertyValidationError(
                f"El valor admite como máximo {self.maximum} caracteres."
            )


@dataclass(frozen=True)
class CompositeValidator:
    validators: tuple[PropertyValidator, ...]

    def __init__(self, validators):
        object.__setattr__(self, "validators", tuple(validators))

    def validate(self, value: Any) -> None:
        for validator in self.validators:
            validator.validate(value)
