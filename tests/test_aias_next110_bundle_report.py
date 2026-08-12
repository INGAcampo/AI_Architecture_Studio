from aias_next110_bundle_report import BundleReport

def test_report_preserves_bundle_status():
    result = BundleReport().generate({"valid": True, "count": 2})
    assert result["report"] == "AIAS-NEXT-110"
    assert result["verification"]["valid"] is True
    assert result["external_validity"] is False
