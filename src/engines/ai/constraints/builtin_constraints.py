from __future__ import annotations
from math import hypot
from typing import Mapping

from .constraint import Constraint, ConstraintKind


class EqualityConstraint(Constraint):
    kind = ConstraintKind.EQUALITY

    def __init__(self, constraint_id: str, left: str, right: str, **kwargs) -> None:
        super().__init__(constraint_id, **kwargs)
        self.left = left
        self.right = right

    def residual(self, values: Mapping[str, float]) -> float:
        return values[self.left] - values[self.right]

    def variables(self) -> tuple[str, ...]:
        return (self.left, self.right)

    def project(self, values: dict[str, float]) -> bool:
        target = (values[self.left] + values[self.right]) / 2.0
        changed = values[self.left] != target or values[self.right] != target
        values[self.left] = target
        values[self.right] = target
        return changed


class FixedValueConstraint(Constraint):
    kind = ConstraintKind.FIXED

    def __init__(self, constraint_id: str, variable: str, target: float, **kwargs) -> None:
        super().__init__(constraint_id, **kwargs)
        self.variable = variable
        self.target = float(target)

    def residual(self, values: Mapping[str, float]) -> float:
        return values[self.variable] - self.target

    def variables(self) -> tuple[str, ...]:
        return (self.variable,)

    def project(self, values: dict[str, float]) -> bool:
        changed = values[self.variable] != self.target
        values[self.variable] = self.target
        return changed


class MinimumConstraint(Constraint):
    kind = ConstraintKind.MINIMUM

    def __init__(self, constraint_id: str, variable: str, minimum: float, **kwargs) -> None:
        super().__init__(constraint_id, **kwargs)
        self.variable = variable
        self.minimum = float(minimum)

    def residual(self, values: Mapping[str, float]) -> float:
        return min(values[self.variable] - self.minimum, 0.0)

    def variables(self) -> tuple[str, ...]:
        return (self.variable,)

    def project(self, values: dict[str, float]) -> bool:
        if values[self.variable] >= self.minimum:
            return False
        values[self.variable] = self.minimum
        return True


class MaximumConstraint(Constraint):
    kind = ConstraintKind.MAXIMUM

    def __init__(self, constraint_id: str, variable: str, maximum: float, **kwargs) -> None:
        super().__init__(constraint_id, **kwargs)
        self.variable = variable
        self.maximum = float(maximum)

    def residual(self, values: Mapping[str, float]) -> float:
        return max(values[self.variable] - self.maximum, 0.0)

    def variables(self) -> tuple[str, ...]:
        return (self.variable,)

    def project(self, values: dict[str, float]) -> bool:
        if values[self.variable] <= self.maximum:
            return False
        values[self.variable] = self.maximum
        return True


class DistanceConstraint(Constraint):
    kind = ConstraintKind.DISTANCE

    def __init__(
        self,
        constraint_id: str,
        ax: str,
        ay: str,
        bx: str,
        by: str,
        target_distance: float,
        **kwargs,
    ) -> None:
        super().__init__(constraint_id, **kwargs)
        if target_distance < 0:
            raise ValueError("target_distance inválida")
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.target_distance = float(target_distance)

    def residual(self, values: Mapping[str, float]) -> float:
        current = hypot(values[self.bx]-values[self.ax], values[self.by]-values[self.ay])
        return current - self.target_distance

    def variables(self) -> tuple[str, ...]:
        return (self.ax, self.ay, self.bx, self.by)

    def project(self, values: dict[str, float]) -> bool:
        dx = values[self.bx] - values[self.ax]
        dy = values[self.by] - values[self.ay]
        current = hypot(dx, dy)
        if current == 0:
            values[self.bx] = values[self.ax] + self.target_distance
            values[self.by] = values[self.ay]
            return self.target_distance != 0
        scale = self.target_distance / current
        new_bx = values[self.ax] + dx * scale
        new_by = values[self.ay] + dy * scale
        changed = new_bx != values[self.bx] or new_by != values[self.by]
        values[self.bx] = new_bx
        values[self.by] = new_by
        return changed
