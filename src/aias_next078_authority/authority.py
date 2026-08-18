"""Read-only alignment between evidence identifiers and authority records."""
from __future__ import annotations
from typing import Any, Iterable

class AuthorityAlignment:
    def align(self, evidence: Iterable[dict[str, Any]], authorities: Iterable[dict[str, Any]]) -> dict[str, Any]:
        evidence_ids = {str(item.get("id")) for item in evidence if item.get("id") is not None}
        authority_ids = {str(item.get("evidence_id")) for item in authorities if item.get("evidence_id") is not None}
        return {"status": "ALIGNED", "matched": sorted(evidence_ids & authority_ids), "unmatched_evidence": sorted(evidence_ids - authority_ids), "authority_verified": False}
