"""Internal gate for authorization records."""
from __future__ import annotations
from typing import Any, Mapping

class BundleReleaseAuthorizationGate:
    def evaluate(self, record: Mapping[str, Any]) -> dict[str, Any]:
        authorized = record.get("authorization", {}).get("internally_authorized") is True
        return {"gate": "AIAS-NEXT-158", "ready": authorized, "external_approval": False}
