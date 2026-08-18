from structural_platform_evidence.bundle import StructuralEvidenceBundle,evidence_bundle_sha256
from structural_platform_verdict.verdict import make_structural_verdict

def test_clean_evidence_is_accepted():
    b=StructuralEvidenceBundle("M1","AIAS","SOLVER",True,0,0)
    d=make_structural_verdict(b,evidence_bundle_sha256(b))
    assert d.accepted is True

def test_mismatch_is_rejected():
    b=StructuralEvidenceBundle("M1","AIAS","SOLVER",False,1,0)
    d=make_structural_verdict(b,evidence_bundle_sha256(b))
    assert d.accepted is False
    assert d.reason=="comparison_mismatch"

def test_missing_result_is_rejected():
    b=StructuralEvidenceBundle("M1","AIAS","SOLVER",False,0,1)
    d=make_structural_verdict(b,evidence_bundle_sha256(b))
    assert d.reason=="missing_results"
