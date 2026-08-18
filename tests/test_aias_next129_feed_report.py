from aias_next129_feed_report import FeedBundleReadinessReport

def test_report_keeps_bundle_publication_unauthorized():
    result = FeedBundleReadinessReport().generate({"ready": True})
    assert result["report"] == "AIAS-NEXT-129"
    assert result["publish_authorized"] is False
