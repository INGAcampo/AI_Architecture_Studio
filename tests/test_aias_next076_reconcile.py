from aias_next076_reconcile import LedgerReconciler

def test_reconciliation_detects_duplicate_ids():
    result = LedgerReconciler().reconcile([{"id": "E-1"}, {"id": "E-1"}])
    assert result["consistent"] is False
    assert result["duplicate_ids"] == ["E-1"]
