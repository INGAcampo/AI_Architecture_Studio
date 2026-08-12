from aias_evidence_audit import AuditTrail
def test_hash_chain_is_valid_and_tamper_evident():
    trail=AuditTrail(); trail.append("evidence_received","ev-1",{"gate":"EXT-OCCT"}); trail.append("evidence_verified","ev-1",{"authority":False})
    assert trail.verify() is True
    trail.events[0].payload["gate"]="EXT-IFC"
    assert trail.verify() is False
def test_empty_chain_is_valid(): assert AuditTrail().verify() is True
