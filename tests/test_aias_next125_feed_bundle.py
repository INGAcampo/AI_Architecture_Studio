from aias_next125_feed_bundle import FeedEvidenceBundle

def test_bundle_is_deterministic_and_local():
    result = FeedEvidenceBundle().build(["integrity.json", "index.json", "index.json"])
    assert result["reports"] == ["index.json", "integrity.json"]
    assert result["count"] == 2
    assert result["external_publication"] is False
