"""Deterministic metrics for review workflow records."""
from __future__ import annotations
from typing import Any, Iterable

class ReviewMetrics:
    def calculate(self, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
        items = list(records)
        accepted = sum(1 for item in items if item.get("decision") == "ACCEPTED")
        rejected = sum(1 for item in items if item.get("decision") == "REJECTED")
        return {"report": "AIAS-NEXT-088", "total": len(items), "accepted": accepted, "rejected": rejected, "pending": len(items) - accepted - rejected, "organizational_maturity_audited": False}
