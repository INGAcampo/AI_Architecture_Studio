"""Deterministic execution report for ordered workflow stages."""
from __future__ import annotations
from typing import Any, Iterable

class WorkflowReport:
    REQUIRED = ("INTAKE", "VALIDATION", "DECISION")
    def generate(self, completed: Iterable[str]) -> dict[str, Any]:
        stages = list(completed)
        ordered = stages == [stage for stage in self.REQUIRED if stage in stages]
        return {"report": "AIAS-NEXT-087", "completed": stages, "ordered": ordered, "complete": ordered and len(stages) == len(self.REQUIRED), "approved": False}
