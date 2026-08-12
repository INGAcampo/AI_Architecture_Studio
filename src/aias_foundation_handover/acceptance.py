"""Lifecycle and construction acceptance gates for digital handovers."""
from __future__ import annotations

def evaluate(verification: dict) -> dict:
    """Evaluate completeness, integrity, issue closure and professional approval."""
    manifest = verification["manifest"]
    issues_closed = not any(issue["status"] == "OPEN" for issue in manifest.get("issues", []))
    gates = {
        "completeness": bool(manifest["completeness"]["complete"]),
        "integrity": bool(verification["valid"]),
        "issues_closed": issues_closed,
        "professional_approval": manifest["delivery_status"] == "CONSTRUCTION_APPROVED",
    }
    return {"gates": gates, "lifecycle_accepted": gates["completeness"] and gates["integrity"] and gates["issues_closed"], "construction_accepted": all(gates.values())}
