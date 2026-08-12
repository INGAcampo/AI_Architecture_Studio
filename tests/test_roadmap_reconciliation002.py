import json
from pathlib import Path

from aias_roadmap_audit import HistoricalDecisionReconciler

ROOT = Path(__file__).resolve().parents[1]


def test_reconciliation_validates_approved_decisions_and_evidence():
    report = HistoricalDecisionReconciler().reconcile(ROOT)
    assert report["status"] == "VALID"
    assert report["issues"] == []
    assert report["approved_decisions_assessed"] == 19
    evidenced = next(item for item in report["items"] if item["decision_id"] == "GEN-001")
    assert evidenced["verified_evidence"] and not evidenced["missing_evidence"]


def test_reconciliation_selects_first_approved_technical_gap():
    report = HistoricalDecisionReconciler().reconcile(ROOT)
    assert report["technical_priority_queue"][0] == "GEN-009"
    assert report["next"].startswith("I18N-CORE-005")
    assert "EXP-COMMS-001" in report["deferred_macrodeliveries"]


def test_report_hash_is_reproducible():
    first = HistoricalDecisionReconciler().reconcile(ROOT)
    second = HistoricalDecisionReconciler().reconcile(ROOT)
    assert first["sha256"] == second["sha256"]
    assert len(first["sha256"]) == 64


def test_evidenced_item_with_missing_path_fails_closed(tmp_path):
    (tmp_path / "engineering/aias/history/chat01").mkdir(parents=True)
    register = {"decisions":[{"id":"GEN-X","status":"APPROVED"}]}
    gaps = {"items":[{"decision_id":"GEN-X","status":"EVIDENCED","evidence":["missing"]}],"priority_recommendations":[]}
    (tmp_path / "engineering/aias/history/chat01/CHAT01_DECISION_REGISTER.json").write_text(json.dumps(register), encoding="utf-8")
    (tmp_path / "engineering/aias/history/chat01/CHAT01_MATERIALIZATION_GAP.json").write_text(json.dumps(gaps), encoding="utf-8")
    report = HistoricalDecisionReconciler().reconcile(tmp_path)
    assert report["status"] == "INVALID" and "GEN-X:evidence_missing" in report["issues"]
