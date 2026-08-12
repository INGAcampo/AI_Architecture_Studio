from aias_next124_feed_index_report import FeedIndexIntegrityReport

def test_report_preserves_index_integrity():
    result = FeedIndexIntegrityReport().generate({"valid": True, "sha256": "d" * 64})
    assert result["report"] == "AIAS-NEXT-124"
    assert result["integrity"]["valid"] is True
    assert result["external_validity"] is False
