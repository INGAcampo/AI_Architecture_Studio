from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .geometry import (
    equal_length,
    horizontal,
    parallel,
    perpendicular,
    point_distance,
    points_close,
    vertical,
)
from .store import ConstraintGeometryStore
from .types import (
    ConstraintDefinition,
    ConstraintKind,
    ConstraintPoint,
    ConstraintSegment,
    ConstraintStatus,
)


@dataclass(frozen=True, slots=True)
class ConstraintEvaluation:
    constraint_id: str
    status: ConstraintStatus
    satisfied: bool
    residual: float = 0.0
    message: str = ""


class ConstraintEvaluator:
    def __init__(self, store: ConstraintGeometryStore, tolerance: float = 1e-6) -> None:
        if tolerance <= 0:
            raise ValueError("tolerance debe ser positiva")
        self.store = store
        self.tolerance = tolerance

    def evaluate(self, constraint: ConstraintDefinition) -> ConstraintEvaluation:
        if not constraint.enabled:
            constraint.status = ConstraintStatus.DISABLED
            constraint.message = "Restricción deshabilitada"
            return ConstraintEvaluation(
                constraint.constraint_id,
                ConstraintStatus.DISABLED,
                True,
                0.0,
                constraint.message,
            )

        try:
            values = [
                self.store.get_element(target.object_id, target.element)
                for target in constraint.targets
            ]
            satisfied, residual, message = self._evaluate_kind(constraint, values)
            status = (
                ConstraintStatus.SATISFIED
                if satisfied
                else ConstraintStatus.VIOLATED
            )
        except (KeyError, TypeError, ValueError) as exc:
            satisfied = False
            residual = float("inf")
            status = ConstraintStatus.CONFLICT
            message = str(exc)

        constraint.status = status
        constraint.message = message
        return ConstraintEvaluation(
            constraint.constraint_id,
            status,
            satisfied,
            residual,
            message,
        )

    def _evaluate_kind(
        self,
        constraint: ConstraintDefinition,
        values: list[Any],
    ) -> tuple[bool, float, str]:
        kind = constraint.kind
        tol = self.tolerance

        if kind is ConstraintKind.HORIZONTAL:
            segment = self._segment(values, 1)
            residual = abs(segment.dy) + abs(segment.dz)
            return horizontal(segment, tol), residual, "Horizontal"

        if kind is ConstraintKind.VERTICAL:
            segment = self._segment(values, 1)
            residual = abs(segment.dx) + abs(segment.dz)
            return vertical(segment, tol), residual, "Vertical"

        if kind is ConstraintKind.PARALLEL:
            a, b = self._segments(values, 2)
            residual = abs(a.dx * b.dy - a.dy * b.dx)
            return parallel(a, b, tol), residual, "Paralela"

        if kind is ConstraintKind.PERPENDICULAR:
            a, b = self._segments(values, 2)
            residual = abs(a.dx * b.dx + a.dy * b.dy + a.dz * b.dz)
            return perpendicular(a, b, tol), residual, "Perpendicular"

        if kind is ConstraintKind.COINCIDENT:
            a, b = self._points(values, 2)
            residual = point_distance(a, b)
            return points_close(a, b, tol), residual, "Coincidente"

        if kind is ConstraintKind.EQUAL_LENGTH:
            a, b = self._segments(values, 2)
            residual = abs(a.length - b.length)
            return equal_length(a, b, tol), residual, "Longitudes iguales"

        if kind is ConstraintKind.LOCK_POINT:
            current, expected = self._points(values, 2)
            residual = point_distance(current, expected)
            return points_close(current, expected, tol), residual, "Punto bloqueado"

        if kind in {ConstraintKind.DISTANCE, ConstraintKind.OFFSET}:
            if constraint.value is None:
                raise ValueError("La restricción requiere value")
            a, b = self._points(values, 2)
            actual = point_distance(a, b)
            residual = abs(actual - constraint.value)
            return residual <= tol, residual, f"Distancia {constraint.value}"

        raise ValueError(f"Tipo no soportado: {kind}")

    @staticmethod
    def _segment(values: list[Any], count: int) -> ConstraintSegment:
        segments = ConstraintEvaluator._segments(values, count)
        return segments[0]

    @staticmethod
    def _segments(values: list[Any], count: int) -> tuple[ConstraintSegment, ...]:
        if len(values) != count or not all(isinstance(v, ConstraintSegment) for v in values):
            raise TypeError(f"Se esperaban {count} segmentos")
        return tuple(values)

    @staticmethod
    def _points(values: list[Any], count: int) -> tuple[ConstraintPoint, ...]:
        if len(values) != count or not all(isinstance(v, ConstraintPoint) for v in values):
            raise TypeError(f"Se esperaban {count} puntos")
        return tuple(values)
