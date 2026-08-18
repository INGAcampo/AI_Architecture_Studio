from datetime import date
from aias_structural_codes_program import ProfessionalReleaseGate,ProfessionalSignoff,REQUIRED_DELIVERABLES,StructuralReleaseCandidate


def candidate(signoff=True,issues=()):
    approval=ProfessionalSignoff("Engineer A","REG-100","BO",date(2026,8,3),"signed://approval") if signoff else None
    deliverables=tuple((kind,f"sha256://{kind.lower()}") for kind in sorted(REQUIRED_DELIVERABLES))
    return StructuralReleaseCandidate("REL-1","PROJECT-1","R01","BO",date(2026,8,3),("BO-CONCRETE-1",),("sha256://benchmark",),deliverables,issues,approval)


def test_complete_professionally_signed_release_can_be_authorized():
    decision=ProfessionalReleaseGate().evaluate(candidate())
    assert decision.status=="AUTHORIZED"
    assert decision.issues==()
    assert decision.construction_release_authorized is True
    assert len(decision.candidate_sha256)==64


def test_release_fails_closed_without_professional_signoff():
    decision=ProfessionalReleaseGate().evaluate(candidate(signoff=False))
    assert decision.status=="BLOCKED"
    assert "qualified_professional_signoff_required" in decision.issues
    assert decision.construction_release_authorized is False


def test_release_rejects_missing_deliverables_and_critical_issues():
    item=candidate(issues=("unstable_model",))
    item=StructuralReleaseCandidate(item.release_id,item.project_id,item.building_revision,item.jurisdiction,item.issued_on,item.normative_pack_ids,item.accepted_benchmark_evidence,item.deliverables[:-1],item.unresolved_critical_issues,item.signoff)
    decision=ProfessionalReleaseGate().evaluate(item)
    assert any(issue.startswith("missing_deliverables") for issue in decision.issues)
    assert "unresolved_critical_issues" in decision.issues


def test_foreign_jurisdiction_signoff_is_rejected():
    item=candidate();foreign=ProfessionalSignoff("Engineer A","REG-100","OTHER",date(2026,8,3),"signed://approval")
    item=StructuralReleaseCandidate(item.release_id,item.project_id,item.building_revision,item.jurisdiction,item.issued_on,item.normative_pack_ids,item.accepted_benchmark_evidence,item.deliverables,item.unresolved_critical_issues,foreign)
    assert "signoff_jurisdiction_mismatch" in ProfessionalReleaseGate().evaluate(item).issues
