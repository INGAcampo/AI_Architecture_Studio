"""Deterministic local bundle metadata for feed evidence."""
from __future__ import annotations
from typing import Any, Iterable

class FeedEvidenceBundle:
    def build(self, reports: Iterable[str]) -> dict[str, Any]:
        items = sorted(set(reports))
        return {"bundle": "AIAS-NEXT-125", "reports": items, "count": len(items), "external_publication": False}
