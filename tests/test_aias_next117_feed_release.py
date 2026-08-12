from aias_next117_feed_release import FeedRelease

def test_feed_release_is_reproducible_and_local():
    result = FeedRelease().build(["feed.json", "report.json", "feed.json"])
    assert result["artifacts"] == ["feed.json", "report.json"]
    assert result["reproducible"] is True
    assert result["published_externally"] is False
