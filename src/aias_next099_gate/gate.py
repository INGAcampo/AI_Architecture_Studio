"""Local release readiness gate with safe external-publication default."""
from __future__ import annotations
from typing import Any, Mapping

class ReleaseReadiness:
    def evaluate(self, verification: Mapping[str, Any], checksums_present: bool) -> dict[str, Any]:
        ready = bool(verification.get("unique")) and bool(verification.get("reproducible")) and checksums_present
        return {"report": "AIAS-NEXT-099", "ready": ready, "checksums_present": checksums_present, "publish_authorized": False}
