from aias_next102_index_report import IndexReport

def test_report_preserves_index():
    result = IndexReport().generate({"count": 2, "artifacts": ["a", "b"]})
    assert result["report"] == "AIAS-NEXT-102"
    assert result["index"]["count"] == 2
    assert result["external_publication"] is False
