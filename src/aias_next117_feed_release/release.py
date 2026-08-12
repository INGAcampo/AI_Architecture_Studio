"""Reproducible local release metadata for the Dashboard feed."""
from __future__ import annotations
from typing import Any, Iterable

class FeedRelease:
    def build(self, artifacts: Iterable[str]) -> dict[str, Any]:
        items = sorted(set(artifacts))
        return {"release": "AIAS-NEXT-117", "artifacts": items, "reproducible": True, "published_externally": False}
