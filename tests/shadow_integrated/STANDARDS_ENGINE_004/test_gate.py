from standards_engine_gate.gate import evaluate_standards_gate

def test_gate_accepts_only_fully_verified_applicable_pack():
    assert evaluate_standards_gate(provenance_valid=True,applicable=True,source_verified=True).accepted is True

def test_unverified_source_is_blocked():
    d=evaluate_standards_gate(provenance_valid=True,applicable=True,source_verified=False)
    assert d.accepted is False
    assert d.reason=="source_not_verified"

def test_nonapplicable_pack_is_blocked():
    assert evaluate_standards_gate(provenance_valid=True,applicable=False,source_verified=True).accepted is False
