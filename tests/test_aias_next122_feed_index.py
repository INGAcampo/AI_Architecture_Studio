from aias_next122_feed_index import FeedArtifactIndex

def test_feed_index_is_sorted_unique():
    result = FeedArtifactIndex().build(["report.json", "feed.json", "feed.json"])
    assert result["artifacts"] == ["feed.json", "report.json"]
    assert result["count"] == 2
    assert result["external_publication"] is False
