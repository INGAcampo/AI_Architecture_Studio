"""Validation-only audit for decision records."""
from __future__ import annotations
from typing import Any, Iterable

class DecisionAudit:
    def audit(self, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
        items = list(records)
        valid = all(item.get("evidence_id") and item.get("decision") in {"PENDING_REVIEW", "ACCEPTED", "REJECTED"} for item in items)
        return {"report": "AIAS-NEXT-085", "record_count": len(items), "valid": valid, "certification": False}
