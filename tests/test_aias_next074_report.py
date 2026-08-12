from aias_next074_report import PublicationReport

def test_report_preserves_missing_state(tmp_path):
    result = PublicationReport(tmp_path / "publication.pdf").generate()
    assert result["report"] == "AIAS-NEXT-074"
    assert result["observation"]["status"] == "NO_PUBLICATION"
    assert result["approval"] is False
