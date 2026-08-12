"""Deterministic index builder for feed release artifacts."""
from __future__ import annotations
from typing import Any, Iterable

class FeedArtifactIndex:
    def build(self, artifacts: Iterable[str]) -> dict[str, Any]:
        items = sorted(set(artifacts))
        return {"index": "AIAS-NEXT-122", "artifacts": items, "count": len(items), "external_publication": False}
