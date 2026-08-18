from aias_next121_feed_report import FeedReadinessReport

def test_report_preserves_gate_boundary():
    result = FeedReadinessReport().generate({"ready": True})
    assert result["report"] == "AIAS-NEXT-121"
    assert result["publish_authorized"] is False
