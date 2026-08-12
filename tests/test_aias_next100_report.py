from aias_next100_report import ReadinessReport

def test_report_keeps_publication_unauthorized():
    result = ReadinessReport().generate({"ready": True})
    assert result["report"] == "AIAS-NEXT-100"
    assert result["publish_authorized"] is False
