from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class ConstraintKind(str, Enum):
    EQUALITY = "equality"
    FIXED = "fixed"
    MINIMUM = "minimum"
    MAXIMUM = "maximum"
    DISTANCE = "distance"
    CUSTOM = "custom"


class ConstraintStatus(str, Enum):
    SATISFIED = "satisfied"
    VIOLATED = "violated"
    DISABLED = "disabled"


@dataclass(frozen=True, slots=True)
class ConstraintViolation:
    constraint_id: str
    message: str
    residual: float
    involved_variables: tuple[str, ...]


class Constraint(ABC):
    constraint_id: str
    kind: ConstraintKind = ConstraintKind.CUSTOM
    enabled: bool = True
    tolerance: float = 1e-6

    def __init__(
        self,
        constraint_id: str,
        *,
        enabled: bool = True,
        tolerance: float = 1e-6,
    ) -> None:
        if not constraint_id.strip():
            raise ValueError("constraint_id es obligatorio")
        if tolerance <= 0:
            raise ValueError("tolerance debe ser positiva")
        self.constraint_id = constraint_id
        self.enabled = enabled
        self.tolerance = tolerance

    @abstractmethod
    def residual(self, values: Mapping[str, float]) -> float:
        raise NotImplementedError

    @abstractmethod
    def variables(self) -> tuple[str, ...]:
        raise NotImplementedError

    @abstractmethod
    def project(self, values: dict[str, float]) -> bool:
        raise NotImplementedError

    def status(self, values: Mapping[str, float]) -> ConstraintStatus:
        if not self.enabled:
            return ConstraintStatus.DISABLED
        return (
            ConstraintStatus.SATISFIED
            if abs(self.residual(values)) <= self.tolerance
            else ConstraintStatus.VIOLATED
        )

    def violation(self, values: Mapping[str, float]) -> ConstraintViolation | None:
        if self.status(values) is not ConstraintStatus.VIOLATED:
            return None
        residual = self.residual(values)
        return ConstraintViolation(
            constraint_id=self.constraint_id,
            message=f"Restricción incumplida: residual={residual:.6g}",
            residual=residual,
            involved_variables=self.variables(),
        )
