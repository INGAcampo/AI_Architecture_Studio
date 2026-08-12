"""Read-only verification of feed bundle report identifiers."""
from __future__ import annotations
from typing import Any, Iterable

class FeedBundleVerifier:
    def verify(self, reports: Iterable[str]) -> dict[str, Any]:
        items = list(reports)
        unique = len(items) == len(set(items))
        return {"report": "AIAS-NEXT-126", "count": len(items), "unique": unique, "valid": unique, "external_validity": False}
