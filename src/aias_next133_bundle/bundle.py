"""Deterministic local evidence bundling for release traceability."""

from __future__ import annotations

from typing import Any, Iterable


class BundleReleaseEvidence:
    """Build a stable, local-only index of bundle reports."""

    def build(self, reports: Iterable[str]) -> dict[str, Any]:
        items = sorted({str(report) for report in reports})
        return {
            "bundle": "AIAS-NEXT-133",
            "reports": items,
            "count": len(items),
            "external_publication": False,
        }
