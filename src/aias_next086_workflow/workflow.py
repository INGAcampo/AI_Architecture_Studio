"""Small deterministic workflow for evidence review stages."""
from __future__ import annotations
from typing import Any

class ReviewWorkflow:
    STAGES = ("INTAKE", "VALIDATION", "DECISION")
    def advance(self, current: str) -> dict[str, Any]:
        if current not in self.STAGES:
            raise ValueError(f"unsupported stage: {current}")
        index = self.STAGES.index(current)
        next_stage = self.STAGES[index + 1] if index + 1 < len(self.STAGES) else "COMPLETE"
        return {"current": current, "next": next_stage, "approved": False}
