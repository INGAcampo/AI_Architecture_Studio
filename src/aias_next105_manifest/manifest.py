"""Deterministic manifest builder for release evidence."""
from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Any, Iterable

class EvidenceManifest:
    def build(self, paths: Iterable[str | Path]) -> dict[str, Any]:
        entries = []
        for raw in sorted({str(path) for path in paths}):
            path = Path(raw)
            entries.append({"path": raw, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        return {"manifest": "AIAS-NEXT-105", "entries": entries, "external_publication": False}
