"""Deterministic local bundle metadata builder."""
from __future__ import annotations
from typing import Any, Iterable

class EvidenceBundle:
    def build(self, reports: Iterable[str]) -> dict[str, Any]:
        items = sorted(set(reports))
        return {"bundle": "AIAS-NEXT-108", "reports": items, "count": len(items), "external_publication": False}
