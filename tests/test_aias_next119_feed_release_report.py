from aias_next119_feed_release_report import FeedReleaseReport

def test_report_preserves_release_verification():
    result = FeedReleaseReport().generate({"unique": True, "reproducible": True})
    assert result["report"] == "AIAS-NEXT-119"
    assert result["verification"]["reproducible"] is True
    assert result["published_externally"] is False
