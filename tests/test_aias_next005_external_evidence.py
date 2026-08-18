import hashlib
import pytest
from aias_external_evidence import EvidenceIntake, EvidenceRecord, EvidenceStatus
def test_evidence_requires_hash_and_authority_before_eligibility():
    content=b"authorized source placeholder"; intake=EvidenceIntake(); record=EvidenceRecord("ev-1","EXT-OCCT","vendor","license",hashlib.sha256(content).hexdigest()); intake.receive(record)
    assert intake.verify("ev-1",content).status == EvidenceStatus.PENDING_AUTHORITY
    assert intake.roadmap_eligible("ev-1") is False
    assert intake.verify("ev-1",content,authority_confirmed=True).status == EvidenceStatus.VERIFIED
    assert intake.roadmap_eligible("ev-1") is True
def test_hash_mismatch_fails_closed():
    intake=EvidenceIntake(); intake.receive(EvidenceRecord("ev-2","EXT-IFC","authority","schema","0"*64))
    with pytest.raises(ValueError,match="evidence_hash_mismatch"): intake.verify("ev-2",b"different")
