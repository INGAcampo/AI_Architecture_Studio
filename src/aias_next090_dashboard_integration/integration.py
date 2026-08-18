"""Integrate a validated operational feed into a dashboard model."""
from __future__ import annotations
from typing import Any, Mapping

class DashboardIntegration:
    def integrate(self, feed: Mapping[str, Any]) -> dict[str, Any]:
        if feed.get("classification") != "OPERATIONAL_ONLY":
            raise ValueError("feed must be operational-only")
        return {"dashboard_component": "EVIDENCE_REVIEW_METRICS", "feed": dict(feed), "audited": False}
