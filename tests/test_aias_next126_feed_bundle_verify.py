from aias_next126_feed_bundle_verify import FeedBundleVerifier

def test_verifier_flags_duplicate_reports():
    result = FeedBundleVerifier().verify(["index", "index"])
    assert result["unique"] is False
    assert result["valid"] is False
    assert result["external_validity"] is False
