"""Stable local reporting for manifest verification."""

from __future__ import annotations

from typing import Any, Mapping


class BundleManifestVerificationReport:
    """Wrap manifest verification output without adding authority."""

    def generate(self, verification: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "report": "AIAS-NEXT-145",
            "verification": dict(verification),
            "local_only": True,
        }
