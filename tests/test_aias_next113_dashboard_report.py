from aias_next113_dashboard_report import FeedReport

def test_report_preserves_feed_validation():
    result = FeedReport().generate({"valid": True, "audited": False})
    assert result["report"] == "AIAS-NEXT-113"
    assert result["validation"]["valid"] is True
    assert result["certification"] is False
