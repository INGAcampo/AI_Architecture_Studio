from aias_next093_export import EvidenceExport

def test_export_has_stable_digest():
    result = EvidenceExport().export({"component": "EVIDENCE_REVIEW_METRICS"})
    assert result["export"] == "AIAS-NEXT-093"
    assert len(result["sha256"]) == 64
    assert result["certification"] is False
