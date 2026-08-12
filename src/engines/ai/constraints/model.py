from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

from .constraint import Constraint


@dataclass(slots=True)
class ConstraintVariable:
    variable_id: str
    value: float
    locked: bool = False
    minimum: float | None = None
    maximum: float | None = None

    def __post_init__(self) -> None:
        if not self.variable_id.strip():
            raise ValueError("variable_id es obligatorio")
        self.value = float(self.value)
        self.clamp()

    def clamp(self) -> None:
        if self.minimum is not None and self.value < self.minimum:
            self.value = self.minimum
        if self.maximum is not None and self.value > self.maximum:
            self.value = self.maximum


class ConstraintSystem:
    def __init__(self) -> None:
        self._variables: dict[str, ConstraintVariable] = {}
        self._constraints: dict[str, Constraint] = {}

    def add_variable(self, variable: ConstraintVariable, *, replace: bool = False) -> None:
        if variable.variable_id in self._variables and not replace:
            raise ValueError(f"Variable duplicada: {variable.variable_id}")
        self._variables[variable.variable_id] = variable

    def add_constraint(self, constraint: Constraint, *, replace: bool = False) -> None:
        if constraint.constraint_id in self._constraints and not replace:
            raise ValueError(f"Restricción duplicada: {constraint.constraint_id}")
        self._constraints[constraint.constraint_id] = constraint

    def variable(self, variable_id: str) -> ConstraintVariable:
        return self._variables[variable_id]

    def constraint(self, constraint_id: str) -> Constraint:
        return self._constraints[constraint_id]

    def values(self) -> dict[str, float]:
        return {key: variable.value for key, variable in self._variables.items()}

    def update_values(self, values: dict[str, float]) -> None:
        for variable_id, value in values.items():
            variable = self._variables[variable_id]
            if variable.locked:
                continue
            variable.value = float(value)
            variable.clamp()

    def variables(self) -> tuple[ConstraintVariable, ...]:
        return tuple(self._variables.values())

    def constraints(self) -> tuple[Constraint, ...]:
        return tuple(self._constraints.values())

    def __len__(self) -> int:
        return len(self._constraints)
