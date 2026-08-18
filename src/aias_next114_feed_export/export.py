"""Deterministic export of the operational Dashboard feed."""
from __future__ import annotations
import hashlib, json
from typing import Any, Mapping

class FeedExport:
    def export(self, feed: Mapping[str, Any]) -> dict[str, Any]:
        serialized = json.dumps(dict(feed), sort_keys=True, separators=(",", ":"))
        return {"export": "AIAS-NEXT-114", "feed": dict(feed), "sha256": hashlib.sha256(serialized.encode()).hexdigest(), "certification": False}
