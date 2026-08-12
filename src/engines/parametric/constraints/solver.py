from __future__ import annotations

from dataclasses import dataclass

from .conflicts import ConstraintConflictDetector
from .evaluator import ConstraintEvaluation, ConstraintEvaluator
from .store import ConstraintRepository
from .types import ConstraintStatus


@dataclass(frozen=True, slots=True)
class ConstraintSolveReport:
    evaluations: tuple[ConstraintEvaluation, ...]
    conflict_count: int
    satisfied_count: int
    violated_count: int

    @property
    def success(self) -> bool:
        return self.conflict_count == 0 and self.violated_count == 0


class ConstraintSolver:
    def __init__(
        self,
        repository: ConstraintRepository,
        evaluator: ConstraintEvaluator,
        conflict_detector: ConstraintConflictDetector | None = None,
    ) -> None:
        self.repository = repository
        self.evaluator = evaluator
        self.conflict_detector = conflict_detector or ConstraintConflictDetector()

    def solve(self) -> ConstraintSolveReport:
        enabled = self.repository.enabled()
        conflicts = self.conflict_detector.detect(enabled)
        conflicted_ids = {
            conflict.first_id
            for conflict in conflicts
        } | {
            conflict.second_id
            for conflict in conflicts
        }

        evaluations: list[ConstraintEvaluation] = []
        for constraint in enabled:
            if constraint.constraint_id in conflicted_ids:
                constraint.status = ConstraintStatus.CONFLICT
                constraint.message = "Conflicto detectado"
                evaluations.append(
                    ConstraintEvaluation(
                        constraint.constraint_id,
                        ConstraintStatus.CONFLICT,
                        False,
                        float("inf"),
                        constraint.message,
                    )
                )
            else:
                evaluations.append(self.evaluator.evaluate(constraint))

        satisfied = sum(e.status is ConstraintStatus.SATISFIED for e in evaluations)
        violated = sum(e.status is ConstraintStatus.VIOLATED for e in evaluations)
        return ConstraintSolveReport(
            evaluations=tuple(evaluations),
            conflict_count=len(conflicts),
            satisfied_count=satisfied,
            violated_count=violated,
        )
