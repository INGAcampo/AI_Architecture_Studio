"""Internal gating for verified release packages."""

from __future__ import annotations

from typing import Any, Mapping


class BundleReleasePackageGate:
    """Open only for a valid local package verification result."""

    def evaluate(self, verification: Mapping[str, Any]) -> dict[str, Any]:
        valid = verification.get("verification", {}).get("valid") is True
        return {
            "gate": "AIAS-NEXT-153",
            "ready": valid,
            "reason": "package_valid" if valid else "package_invalid",
            "external_approval": False,
        }
