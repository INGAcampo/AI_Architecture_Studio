"""Digest comparison for canonical feed exports."""
from __future__ import annotations
import hashlib
from typing import Any

class FeedIntegrity:
    def verify(self, serialized: str, expected_sha256: str) -> dict[str, Any]:
        digest = hashlib.sha256(serialized.encode()).hexdigest()
        return {"report": "AIAS-NEXT-115", "match": digest == expected_sha256, "sha256": digest, "external_validity": False}
