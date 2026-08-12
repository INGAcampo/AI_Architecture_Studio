"""Internal readiness gate for a verified bundle manifest."""

from __future__ import annotations

from typing import Any, Mapping


class BundleReleaseReadiness:
    """Evaluate readiness without implying external release authority."""

    def evaluate(self, report: Mapping[str, Any]) -> dict[str, Any]:
        valid = report.get("verification", {}).get("valid") is True
        return {
            "gate": "AIAS-NEXT-146",
            "ready": valid,
            "status": "READY" if valid else "HOLD",
            "external_release": False,
        }
