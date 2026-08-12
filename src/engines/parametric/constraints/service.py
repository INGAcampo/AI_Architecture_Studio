from __future__ import annotations

from typing import Callable

from .conflicts import ConstraintConflictDetector
from .evaluator import ConstraintEvaluator
from .solver import ConstraintSolveReport, ConstraintSolver
from .store import ConstraintGeometryStore, ConstraintRepository
from .types import ConstraintDefinition


class ConstraintService:
    def __init__(
        self,
        *,
        event_dispatcher=None,
        tolerance: float = 1e-6,
    ) -> None:
        self.geometry = ConstraintGeometryStore()
        self.repository = ConstraintRepository()
        self.evaluator = ConstraintEvaluator(self.geometry, tolerance=tolerance)
        self.solver = ConstraintSolver(
            self.repository,
            self.evaluator,
            ConstraintConflictDetector(),
        )
        self.event_dispatcher = event_dispatcher

    def add_constraint(self, constraint: ConstraintDefinition) -> None:
        self.repository.add(constraint)
        self._publish(
            "constraint.added",
            constraint_id=constraint.constraint_id,
            kind=constraint.kind.value,
        )

    def remove_constraint(self, constraint_id: str) -> ConstraintDefinition:
        constraint = self.repository.remove(constraint_id)
        self._publish(
            "constraint.removed",
            constraint_id=constraint_id,
        )
        return constraint

    def evaluate(self, constraint_id: str):
        result = self.evaluator.evaluate(self.repository.get(constraint_id))
        self._publish(
            "constraint.evaluated",
            constraint_id=constraint_id,
            status=result.status.value,
        )
        return result

    def solve(self) -> ConstraintSolveReport:
        report = self.solver.solve()
        self._publish(
            "constraint.solve.completed",
            success=report.success,
            conflicts=report.conflict_count,
            violations=report.violated_count,
        )
        return report

    def _publish(self, name: str, **payload) -> None:
        target = self.event_dispatcher
        if target is None:
            return
        if callable(target):
            target(name, payload)
            return
        dispatch = getattr(target, "dispatch", None)
        if callable(dispatch):
            try:
                dispatch(name, payload)
            except TypeError:
                dispatch({"name": name, "payload": payload})
