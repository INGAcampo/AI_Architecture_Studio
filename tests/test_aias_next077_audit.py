from aias_next077_audit import LedgerAudit

def test_audit_reports_consistent_empty_ledger():
    result = LedgerAudit().audit([])
    assert result["report"] == "AIAS-NEXT-077"
    assert result["reconciliation"]["consistent"] is True
    assert result["external_certification"] is False
