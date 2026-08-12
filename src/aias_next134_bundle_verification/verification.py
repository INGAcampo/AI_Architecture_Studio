"""Deterministic verification for local bundle evidence identifiers."""

from __future__ import annotations

from typing import Any, Iterable


class BundleVerification:
    """Verify that bundle report identifiers are unique and non-empty."""

    def verify(self, reports: Iterable[str]) -> dict[str, Any]:
        items = [str(report) for report in reports]
        non_empty = all(bool(item.strip()) for item in items)
        unique = len(items) == len(set(items))
        return {
            "bundle": "AIAS-NEXT-134",
            "valid": non_empty and unique,
            "unique": unique,
            "non_empty": non_empty,
            "count": len(items),
            "external_claim": False,
        }
