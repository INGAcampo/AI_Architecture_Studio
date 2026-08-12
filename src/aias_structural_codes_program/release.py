"""Fail-closed professional structural production release gate."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
import hashlib
import json


REQUIRED_DELIVERABLES = frozenset({
    "ANALYSIS_MODEL", "CALCULATION_REPORT", "DESIGN_SCHEDULES",
    "STRUCTURAL_DRAWINGS", "SPECIFICATIONS", "REVISION_REGISTER",
})


@dataclass(frozen=True, slots=True)
class ProfessionalSignoff:
    responsible_professional: str
    registration_id: str
    jurisdiction: str
    signed_on: date | None
    approval_reference: str

    def complete(self) -> bool:
        return bool(self.responsible_professional and self.registration_id and self.jurisdiction and self.signed_on and self.approval_reference)


@dataclass(frozen=True, slots=True)
class StructuralReleaseCandidate:
    release_id: str
    project_id: str
    building_revision: str
    jurisdiction: str
    issued_on: date
    normative_pack_ids: tuple[str, ...]
    accepted_benchmark_evidence: tuple[str, ...]
    deliverables: tuple[tuple[str, str], ...]
    unresolved_critical_issues: tuple[str, ...]
    signoff: ProfessionalSignoff | None

    def integrity_sha256(self) -> str:
        payload=json.dumps(asdict(self),sort_keys=True,separators=(",",":"),default=str,ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class StructuralReleaseDecision:
    release_id: str
    candidate_sha256: str
    status: str
    issues: tuple[str, ...]
    construction_release_authorized: bool


class ProfessionalReleaseGate:
    """Authorize only complete evidence reviewed by a responsible professional."""

    def evaluate(self, candidate: StructuralReleaseCandidate) -> StructuralReleaseDecision:
        issues: list[str] = []
        if not all((candidate.release_id,candidate.project_id,candidate.building_revision,candidate.jurisdiction)):
            issues.append("release_identity_incomplete")
        if not candidate.normative_pack_ids:
            issues.append("accepted_normative_packs_required")
        if not candidate.accepted_benchmark_evidence:
            issues.append("accepted_independent_benchmarks_required")
        kinds=[kind for kind,_ in candidate.deliverables]
        if len(kinds)!=len(set(kinds)):
            issues.append("duplicate_deliverable_kind")
        missing=sorted(REQUIRED_DELIVERABLES-set(kinds))
        if missing:
            issues.append(f"missing_deliverables:{missing}")
        if any(not locator for _,locator in candidate.deliverables):
            issues.append("deliverable_locator_required")
        if candidate.unresolved_critical_issues:
            issues.append("unresolved_critical_issues")
        if candidate.signoff is None or not candidate.signoff.complete():
            issues.append("qualified_professional_signoff_required")
        elif candidate.signoff.jurisdiction != candidate.jurisdiction:
            issues.append("signoff_jurisdiction_mismatch")
        authorized=not issues
        return StructuralReleaseDecision(candidate.release_id,candidate.integrity_sha256(),"AUTHORIZED" if authorized else "BLOCKED",tuple(issues),authorized)
