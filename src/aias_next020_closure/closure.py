from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ClosureResult:
    status: str
    lessons_required: bool
    reason: str


class ClosureGate:
    def __init__(self, review_package: str | Path, handoff: str | Path):
        self.review_package = Path(review_package)
        self.handoff = Path(handoff)

    def evaluate(self) -> ClosureResult:
        if not self.review_package.exists() or not self.handoff.exists():
            return ClosureResult("OPEN_COLLECTION", True, "review package or handoff absent")
        review = json.loads(self.review_package.read_text(encoding="utf-8"))
        handoff = json.loads(self.handoff.read_text(encoding="utf-8"))
        approved = handoff.get("approval_status") == "APPROVED_BY_INDEPENDENT_REVIEWER" and bool(handoff.get("reviewer_reference"))
        if review.get("review_ready") and approved:
            return ClosureResult("CLOSE_WITH_LESSONS", True, "evidence threshold and explicit approval met")
        return ClosureResult("OPEN_COLLECTION", True, "human approval or evidence threshold pending")
