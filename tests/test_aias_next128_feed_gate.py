from aias_next128_feed_gate import FeedBundleReadiness

def test_gate_requires_valid_unique_bundle_and_checksum():
    result = FeedBundleReadiness().evaluate({"unique": True, "valid": True}, True)
    assert result["ready"] is True
    assert result["publish_authorized"] is False
