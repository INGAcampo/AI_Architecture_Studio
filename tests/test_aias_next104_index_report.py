from aias_next104_index_report import IndexIntegrityReport

def test_report_preserves_integrity_boundary():
    result = IndexIntegrityReport().generate({"valid": True, "sha256": "b" * 64})
    assert result["report"] == "AIAS-NEXT-104"
    assert result["integrity"]["valid"] is True
    assert result["external_validity"] is False
