from aias_next095_integrity_report import IntegrityReport

def test_report_preserves_integrity_result():
    result = IntegrityReport().generate({"match": True, "sha256": "a" * 64})
    assert result["report"] == "AIAS-NEXT-095"
    assert result["verification"]["match"] is True
    assert result["external_validity"] is False
