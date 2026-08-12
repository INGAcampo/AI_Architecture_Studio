from aias_next120_feed_gate import FeedReadiness

def test_gate_requires_reproducible_verification_and_checksum():
    result = FeedReadiness().evaluate({"unique": True, "reproducible": True}, True)
    assert result["ready"] is True
    assert result["publish_authorized"] is False
