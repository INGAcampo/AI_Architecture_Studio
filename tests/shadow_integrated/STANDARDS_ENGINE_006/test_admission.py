from standards_engine_admission.admission import evaluate_rule_pack_admission

def test_fully_verified_pack_is_accepted():
    d=evaluate_rule_pack_admission(
        source_evidence_accepted=True,
        provenance_valid=True,
        applicability_passed=True,
        pack_hash_valid=True,
    )
    assert d.accepted is True

def test_source_rejection_blocks_pack():
    d=evaluate_rule_pack_admission(
        source_evidence_accepted=False,
        provenance_valid=True,
        applicability_passed=True,
        pack_hash_valid=True,
    )
    assert d.accepted is False
    assert d.reason=="source_evidence_rejected"

def test_hash_failure_blocks_pack():
    d=evaluate_rule_pack_admission(
        source_evidence_accepted=True,
        provenance_valid=True,
        applicability_passed=True,
        pack_hash_valid=False,
    )
    assert d.accepted is False
    assert d.reason=="pack_hash_invalid"
