"""Explicit gate for external evidence authorization."""
from __future__ import annotations
from typing import Any

class EvidenceGate:
    """Classify observations; never infer authorization or approval."""
    def evaluate(self, observation: dict[str, Any], external_authority: bool = False) -> dict[str, Any]:
        status = "AUTHORIZED_EVIDENCE" if external_authority else "PENDING_EXTERNAL_EVIDENCE"
        return {"status": status, "observation": observation, "approved": False, "authority_verified": external_authority}
