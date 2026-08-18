"""Reproducible release metadata builder."""
from __future__ import annotations
from typing import Any, Iterable

class ReleasePackage:
    def build(self, artifacts: Iterable[str]) -> dict[str, Any]:
        items = sorted(set(artifacts))
        return {"release": "AIAS-NEXT-096", "artifacts": items, "reproducible": True, "published_externally": False}
