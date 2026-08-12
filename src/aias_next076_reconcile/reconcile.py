"""Deterministic, read-only reconciliation of evidence records."""
from __future__ import annotations
from typing import Any, Iterable

class LedgerReconciler:
    def reconcile(self, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
        items = list(records)
        ids = [str(item.get("id", "")) for item in items]
        duplicates = sorted({value for value in ids if value and ids.count(value) > 1})
        return {"status": "RECONCILED", "record_count": len(items), "duplicate_ids": duplicates, "consistent": not duplicates}
