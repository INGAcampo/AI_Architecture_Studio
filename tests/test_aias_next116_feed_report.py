from aias_next116_feed_report import FeedIntegrityReport

def test_report_preserves_feed_digest_state():
    result = FeedIntegrityReport().generate({"match": True, "sha256": "c" * 64})
    assert result["report"] == "AIAS-NEXT-116"
    assert result["verification"]["match"] is True
    assert result["external_validity"] is False
