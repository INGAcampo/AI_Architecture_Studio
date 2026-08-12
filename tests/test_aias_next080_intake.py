from aias_next080_intake import EvidenceIntake

def test_intake_requires_source_and_digest():
    result = EvidenceIntake().validate({"id": "E-1"})
    assert result["status"] == "INVALID_INTAKE"
    assert set(result["missing"]) == {"source", "sha256"}
    assert result["approved"] is False
