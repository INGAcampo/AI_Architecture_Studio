from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReconciliationResult:
    status: str
    release_allowed: bool
    reasons: tuple[str, ...]


class ReleaseDecisionReconciler:
    def __init__(self, decision_path: str | Path, governance_path: str | Path):
        self.decision = Path(decision_path)
        self.governance = Path(governance_path)

    def evaluate(self) -> ReconciliationResult:
        if not self.decision.exists() or not self.governance.exists():
            return ReconciliationResult("HOLD", False, ("decision or governance record absent",))
        decision = json.loads(self.decision.read_text(encoding="utf-8"))
        governance = json.loads(self.governance.read_text(encoding="utf-8"))
        reasons = []
        if decision.get("decision") != "APPROVED":
            reasons.append("decision not APPROVED")
        if governance.get("external_gates") != "APPROVED":
            reasons.append("external gates not APPROVED")
        if governance.get("production_approval") != "GRANTED":
            reasons.append("production approval not GRANTED")
        return ReconciliationResult("RELEASE_ALLOWED" if not reasons else "HOLD", not reasons, tuple(reasons))
