from aias_next132_bundle_index_report import BundleIndexIntegrityReport

def test_report_preserves_bundle_index_integrity():
    result = BundleIndexIntegrityReport().generate({"valid": True, "sha256": "e" * 64})
    assert result["report"] == "AIAS-NEXT-132"
    assert result["integrity"]["valid"] is True
    assert result["external_validity"] is False
