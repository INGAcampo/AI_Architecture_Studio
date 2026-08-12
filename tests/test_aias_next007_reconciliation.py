import json
from pathlib import Path
from aias_roadmap_reconciliation import RoadmapReconciler
ROOT=Path(__file__).resolve().parents[1]
def test_reconciler_finds_present_and_missing_artifacts():
    result=RoadmapReconciler().reconcile(ROOT,["engineering/aias/roadmap/AIAS_NEXT_STRATEGY.json","does/not/exist.json"],["OCCT"])
    assert result.checked == 2 and len(result.present) == 1 and len(result.missing) == 1 and result.external_pending == ("OCCT",)
    assert result.valid is False
def test_snapshot_preserves_pending_external_gates():
    snapshot=json.loads((ROOT/"engineering/aias/roadmap_reconciliation/ROADMAP_EVIDENCE_SNAPSHOT.json").read_text(encoding="utf-8"))
    assert "IfcOpenShell" in snapshot["external_pending"] and "independent professional review" in snapshot["external_pending"]
