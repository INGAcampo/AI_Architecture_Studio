"""Stable report envelope for feed readiness."""
from __future__ import annotations
from typing import Any, Mapping

class FeedReadinessReport:
    def generate(self, gate: Mapping[str, Any]) -> dict[str, Any]:
        return {"report": "AIAS-NEXT-121", "gate": dict(gate), "publish_authorized": False}
