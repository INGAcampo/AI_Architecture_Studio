from aias_next098_release_report import ReleaseReport

def test_report_preserves_release_boundary():
    result = ReleaseReport().generate({"unique": True, "reproducible": True})
    assert result["report"] == "AIAS-NEXT-098"
    assert result["verification"]["unique"] is True
    assert result["published_externally"] is False
