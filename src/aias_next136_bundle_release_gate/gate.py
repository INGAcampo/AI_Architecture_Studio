"""Local release gating for verified bundle evidence."""

from __future__ import annotations

from typing import Any, Mapping


class BundleReleaseGate:
    """Allow progression only when the local verification is valid."""

    def evaluate(self, verification: Mapping[str, Any]) -> dict[str, Any]:
        valid = verification.get("valid") is True
        return {
            "gate": "AIAS-NEXT-136",
            "ready": valid,
            "reason": "verification_valid" if valid else "verification_invalid",
            "external_approval": False,
        }
