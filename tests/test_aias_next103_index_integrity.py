from aias_next103_index_integrity import IndexIntegrity

def test_integrity_accepts_sorted_unique_index():
    result = IndexIntegrity().verify({"artifacts": ["a", "b"]})
    assert result["valid"] is True
    assert len(result["sha256"]) == 64
    assert result["external_validity"] is False
