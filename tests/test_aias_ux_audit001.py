from pathlib import Path

from aias_ux_audit import audit_repository


ROOT = Path(__file__).resolve().parents[1]


def test_audit_defines_six_professional_journeys():
    report = audit_repository(ROOT)
    assert report["schema"] == "AIAS-UX-AUDIT-1.0"
    assert len(report["journeys"]) == 6
    assert report["usability_validated"] is False


def test_each_journey_has_outcome_metric_and_evidence():
    report = audit_repository(ROOT)
    for journey in report["journeys"]:
        assert journey["outcome"]
        assert journey["target_minutes"] > 0
        assert journey["requirements"]
        assert 0 <= journey["evidence_score"] <= 100


def test_workspace_target_is_versioned_and_migration_ordered():
    import json
    target = json.loads((ROOT / "engineering/aias/experience/AIAS_WORKSPACE2_TARGET_ARCHITECTURE.json").read_text(encoding="utf-8"))
    assert target["architecture_id"] == "AIAS-WORKSPACE-2.0"
    assert len(target["migration_order"]) == 7
    assert "single WorkspaceManager state authority" in target["integration_contracts"]
