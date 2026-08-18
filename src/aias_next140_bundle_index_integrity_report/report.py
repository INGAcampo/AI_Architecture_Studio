"""Stable local reporting for index integrity checks."""

from __future__ import annotations

from typing import Any, Mapping


class BundleIndexIntegrityReport:
    """Wrap an integrity result for downstream local consumers."""

    def generate(self, integrity: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "report": "AIAS-NEXT-140",
            "integrity": dict(integrity),
            "local_only": True,
        }
