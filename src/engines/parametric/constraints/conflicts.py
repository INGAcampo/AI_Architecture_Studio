from __future__ import annotations

from dataclasses import dataclass

from .types import ConstraintDefinition, ConstraintKind


@dataclass(frozen=True, slots=True)
class ConstraintConflict:
    first_id: str
    second_id: str
    reason: str


class ConstraintConflictDetector:
    def detect(
        self,
        constraints: tuple[ConstraintDefinition, ...],
    ) -> tuple[ConstraintConflict, ...]:
        conflicts: list[ConstraintConflict] = []
        for index, first in enumerate(constraints):
            if not first.enabled:
                continue
            first_targets = set(first.targets)
            for second in constraints[index + 1:]:
                if not second.enabled:
                    continue
                if not first_targets.intersection(second.targets):
                    continue
                reason = self._reason(first, second)
                if reason:
                    conflicts.append(
                        ConstraintConflict(
                            first.constraint_id,
                            second.constraint_id,
                            reason,
                        )
                    )
        return tuple(conflicts)

    @staticmethod
    def _reason(
        first: ConstraintDefinition,
        second: ConstraintDefinition,
    ) -> str | None:
        kinds = {first.kind, second.kind}
        if kinds == {ConstraintKind.HORIZONTAL, ConstraintKind.VERTICAL}:
            return "El mismo segmento no puede ser horizontal y vertical"
        if kinds == {ConstraintKind.PARALLEL, ConstraintKind.PERPENDICULAR}:
            return "Los mismos segmentos no pueden ser paralelos y perpendiculares"
        if first.kind in {ConstraintKind.DISTANCE, ConstraintKind.OFFSET} and second.kind in {
            ConstraintKind.DISTANCE,
            ConstraintKind.OFFSET,
        }:
            if first.value is not None and second.value is not None and first.value != second.value:
                return "Distancias incompatibles sobre los mismos targets"
        return None
