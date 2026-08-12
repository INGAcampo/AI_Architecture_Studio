from pathlib import Path

from aias_next033_reconcile import ReleaseDecisionReconciler


def test_reconciliation_holds_with_missing_records(tmp_path: Path):
    result = ReleaseDecisionReconciler(tmp_path / "decision.json", tmp_path / "governance.json").evaluate()
    assert result.release_allowed is False
    assert result.status == "HOLD"
