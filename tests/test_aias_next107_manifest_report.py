from aias_next107_manifest_report import ManifestReport

def test_report_preserves_manifest_status():
    result = ManifestReport().generate({"valid": True, "entries": []})
    assert result["report"] == "AIAS-NEXT-107"
    assert result["verification"]["valid"] is True
    assert result["external_validity"] is False
