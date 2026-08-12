"""Consolidate local release evidence without external claims."""

from __future__ import annotations

from typing import Any, Mapping, Sequence


class BundleReleaseEvidence:
    """Build a stable evidence envelope from local reports."""

    def consolidate(self, reports: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
        return {
            "evidence": "AIAS-NEXT-141",
            "reports": [dict(report) for report in reports],
            "count": len(reports),
            "external_release": False,
        }
