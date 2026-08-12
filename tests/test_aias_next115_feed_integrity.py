from aias_next115_feed_integrity import FeedIntegrity
import hashlib

def test_feed_integrity_matches():
    value = "{}"
    digest = hashlib.sha256(value.encode()).hexdigest()
    result = FeedIntegrity().verify(value, digest)
    assert result["match"] is True
    assert result["external_validity"] is False
