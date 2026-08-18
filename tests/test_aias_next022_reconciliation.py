import json
from pathlib import Path

from aias_next022_reconciliation import MaturityReconciler


def test_reconciliation_preserves_unaudited_level(tmp_path: Path):
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text(json.dumps({"maturity": {"reference_capability_level": 5, "audited_organizational_level": None, "campaign_status": "ACTIVE_EVIDENCE_COLLECTION"}}), encoding="utf-8")
    report = MaturityReconciler(snapshot).reconcile()
    assert report.reference_capability_level == 5
    assert report.audited_organizational_level is None
