from aias_next123_feed_index_integrity import FeedIndexIntegrity

def test_index_integrity_accepts_sorted_unique():
    result = FeedIndexIntegrity().verify({"artifacts": ["a", "b"]})
    assert result["valid"] is True
    assert len(result["sha256"]) == 64
    assert result["external_validity"] is False
