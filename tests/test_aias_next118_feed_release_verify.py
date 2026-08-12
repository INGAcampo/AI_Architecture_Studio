from aias_next118_feed_release_verify import FeedReleaseVerifier

def test_verifier_detects_duplicate_feed_artifacts():
    result = FeedReleaseVerifier().verify(["feed.json", "feed.json"])
    assert result["unique"] is False
    assert result["published_externally"] is False
