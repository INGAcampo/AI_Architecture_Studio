"""Verification of local release package descriptors."""

from __future__ import annotations

from typing import Any, Mapping


class BundleReleasePackageVerification:
    """Check that a package has a coherent artifact list."""

    def verify(self, package: Mapping[str, Any]) -> dict[str, Any]:
        artifacts = package.get("artifacts")
        valid = isinstance(artifacts, list) and package.get("count") == len(artifacts)
        return {
            "verification": "AIAS-NEXT-151",
            "valid": valid,
            "count": len(artifacts) if isinstance(artifacts, list) else 0,
            "external_attestation": False,
        }
