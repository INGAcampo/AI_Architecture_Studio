"""Explicit decision record with safe default."""
from __future__ import annotations
from typing import Any

class DecisionRecord:
    def create(self, evidence_id: str, decision: str = "PENDING_REVIEW", rationale: str = "") -> dict[str, Any]:
        allowed = {"PENDING_REVIEW", "ACCEPTED", "REJECTED"}
        if decision not in allowed:
            raise ValueError(f"unsupported decision: {decision}")
        return {"evidence_id": evidence_id, "decision": decision, "rationale": rationale, "approved": decision == "ACCEPTED"}
