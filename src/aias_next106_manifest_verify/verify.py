"""Read-only verification of evidence manifest digests."""
from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Any, Iterable, Mapping

class ManifestVerifier:
    def verify(self, entries: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
        results = []
        for entry in entries:
            path = Path(str(entry["path"]))
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            results.append({"path": str(path), "match": actual == entry.get("sha256"), "sha256": actual})
        return {"report": "AIAS-NEXT-106", "entries": results, "valid": all(item["match"] for item in results), "external_validity": False}
