from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class RuleVerdict:
    rule_id: str
    status: str
    decision_trace: tuple[str, ...]
    evidence_sha256: str | None

    def to_dict(self) -> dict[str, Any]:
        return {"rule_id": self.rule_id, "status": self.status, "decision_trace": list(self.decision_trace), "evidence_sha256": self.evidence_sha256}


class StandardsPack:
    """Versioned, bounded standards contract for the pilot jurisdiction."""

    def __init__(self, jurisdiction: str = "VE", version: str = "VE-PILOT-001.0") -> None:
        self.jurisdiction = jurisdiction
        self.version = version
        self.rules: dict[str, dict[str, Any]] = {
            "VE-ARCH-DIM-001": {"source": "COVENIN-1756-1", "edition": "2001", "section": "habitability", "scope": "pilot", "kind": "dimensional"},
            "VE-LOAD-001": {"source": "COVENIN-2003-1", "edition": "1986", "section": "dead-live-loads", "scope": "pilot", "kind": "loads"},
            "VE-SEISMIC-001": {"source": "COVENIN-1756-1", "edition": "2001", "section": "seismic-zoning", "scope": "pilot", "kind": "seismic"},
            "VE-WIND-001": {"source": "COVENIN-2003-1", "edition": "1986", "section": "wind", "scope": "pilot", "kind": "wind"},
            "VE-CONCRETE-001": {"source": "COVENIN-1753", "edition": "2006", "section": "reinforced-concrete", "scope": "pilot", "kind": "concrete"},
            "VE-FOUNDATION-001": {"source": "COVENIN-1756-1", "edition": "2001", "section": "foundations", "scope": "pilot", "kind": "foundation"},
        }

    def applicability(self, rule_id: str, context: Mapping[str, Any]) -> str:
        rule = self.rules.get(rule_id)
        if rule is None or context.get("jurisdiction") != self.jurisdiction: return "NOT_APPLICABLE"
        return "APPLICABLE" if (context.get("project") == "PILOT-BUILDING-001" or (context.get("SYNTHETIC_TEST_DATA") is True and context.get("NOT_FOR_CONSTRUCTION") is True)) else "NOT_APPLICABLE"

    def canonical_evidence_sha(self, evidence: Mapping[str, Any]) -> str:
        payload = json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(payload).hexdigest()


class ApplicabilityEngine:
    def __init__(self, pack: StandardsPack) -> None:
        self.pack = pack

    def evaluate(self, rule_id: str, context: Mapping[str, Any], evidence: Mapping[str, Any] | None = None) -> RuleVerdict:
        applicability = self.pack.applicability(rule_id, context)
        trace = [f"pack={self.pack.version}", f"rule={rule_id}", f"applicability={applicability}"]
        if applicability == "NOT_APPLICABLE": return RuleVerdict(rule_id, "NOT_APPLICABLE", tuple(trace), None)
        if evidence is None or not evidence.get("source") or evidence.get("value") is None:
            trace.append("evidence=INSUFFICIENT")
            return RuleVerdict(rule_id, "INSUFFICIENT_EVIDENCE", tuple(trace), None)
        sha = self.pack.canonical_evidence_sha(evidence)
        passed = bool(evidence.get("pass"))
        status = "PASS" if passed else "FAIL"
        trace.append(f"evidence_sha256={sha}")
        return RuleVerdict(rule_id, status, tuple(trace), sha)
