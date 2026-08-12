"""Deterministic JSON export with content digest."""
from __future__ import annotations
import hashlib, json
from typing import Any, Mapping

class EvidenceExport:
    def export(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        serialized = json.dumps(dict(payload), sort_keys=True, separators=(",", ":"))
        return {"export": "AIAS-NEXT-093", "payload": dict(payload), "sha256": hashlib.sha256(serialized.encode()).hexdigest(), "certification": False}
