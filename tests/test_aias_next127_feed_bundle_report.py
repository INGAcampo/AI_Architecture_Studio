from aias_next127_feed_bundle_report import FeedBundleReport

def test_report_preserves_bundle_verification():
    result = FeedBundleReport().generate({"valid": True, "count": 2})
    assert result["report"] == "AIAS-NEXT-127"
    assert result["verification"]["valid"] is True
    assert result["external_validity"] is False
