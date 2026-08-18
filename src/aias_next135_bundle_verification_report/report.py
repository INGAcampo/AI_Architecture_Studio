"""Stable reporting for bundle verification results."""

from __future__ import annotations

from typing import Any, Mapping


class BundleVerificationReport:
    """Wrap verification output without changing its meaning."""

    def generate(self, verification: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "report": "AIAS-NEXT-135",
            "verification": dict(verification),
            "external_publication": False,
        }
