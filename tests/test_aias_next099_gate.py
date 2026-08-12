from aias_next099_gate import ReleaseReadiness

def test_gate_requires_checksums_and_reproducibility():
    result = ReleaseReadiness().evaluate({"unique": True, "reproducible": True}, True)
    assert result["ready"] is True
    assert result["publish_authorized"] is False
