from aias_next075_gate import EvidenceGate

def test_gate_requires_external_authority():
    result = EvidenceGate().evaluate({"status": "PUBLICATION_OBSERVED"})
    assert result["status"] == "PENDING_EXTERNAL_EVIDENCE"
    assert result["approved"] is False
