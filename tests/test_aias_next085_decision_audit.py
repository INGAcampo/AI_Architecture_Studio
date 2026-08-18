from aias_next085_decision_audit import DecisionAudit

def test_audit_rejects_invalid_decision_record():
    result = DecisionAudit().audit([{"evidence_id": "E-1", "decision": "UNKNOWN"}])
    assert result["valid"] is False
    assert result["certification"] is False
