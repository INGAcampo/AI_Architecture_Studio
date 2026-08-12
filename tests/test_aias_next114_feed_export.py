from aias_next114_feed_export import FeedExport

def test_feed_export_has_digest():
    result = FeedExport().export({"classification": "OPERATIONAL_ONLY"})
    assert result["export"] == "AIAS-NEXT-114"
    assert len(result["sha256"]) == 64
    assert result["certification"] is False
