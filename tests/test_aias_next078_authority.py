from aias_next078_authority import AuthorityAlignment

def test_alignment_keeps_unmatched_evidence_explicit():
    result = AuthorityAlignment().align([{"id": "E-1"}], [])
    assert result["matched"] == []
    assert result["unmatched_evidence"] == ["E-1"]
    assert result["authority_verified"] is False
