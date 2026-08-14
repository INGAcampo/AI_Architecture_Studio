from structural_platform_evidence.bundle import StructuralEvidenceBundle,evidence_bundle_sha256

def test_evidence_hash_is_deterministic():
    b=StructuralEvidenceBundle("M1","AIAS","SOLVER-X",True,0,0)
    assert evidence_bundle_sha256(b)==evidence_bundle_sha256(b)
    assert len(evidence_bundle_sha256(b))==64

def test_negative_count_fails_closed():
    b=StructuralEvidenceBundle("M1","AIAS","SOLVER-X",False,-1,0)
    try:
        b.validate()
    except ValueError:
        return
    assert False

def test_blank_engine_fails_closed():
    b=StructuralEvidenceBundle("M1","","SOLVER-X",False,0,0)
    try:
        b.validate()
    except ValueError:
        return
    assert False
