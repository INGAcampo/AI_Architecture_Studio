from aias_next081_intake_report import IntakeReport

def test_report_exposes_missing_fields():
    result = IntakeReport().generate({"id": "E-1"})
    assert result["report"] == "AIAS-NEXT-081"
    assert "source" in result["validation"]["missing"]
    assert result["approved"] is False
