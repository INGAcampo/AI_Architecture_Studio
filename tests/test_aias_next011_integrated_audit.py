from pathlib import Path
from aias_integrated_audit import IntegratedAudit
ROOT=Path(__file__).resolve().parents[1]
def test_integrated_audit_detects_complete_local_contract_set():
    artifacts=("engineering/aias/roadmap/AIAS_NEXT_STRATEGY.json","engineering/aias/release_gate/AIAS_NEXT_003_RELEASE_MANIFEST.json","engineering/aias/external_gates/AIAS_NEXT_004_EXTERNAL_GATE_REGISTRY.json","engineering/aias/external_evidence/AIAS_NEXT_005_SPEC.json","engineering/aias/evidence_audit/AIAS_NEXT_006_SPEC.json","engineering/aias/roadmap_reconciliation/AIAS_NEXT_007_SPEC.json","engineering/aias/release_promotion/AIAS_NEXT_008_SPEC.json","engineering/aias/governance_campaign/AIAS_NEXT_009_SPEC.json","engineering/aias/continuity_watch/AIAS_NEXT_010_SPEC.json")
    report=IntegratedAudit().run(ROOT,artifacts,("OCCT","IfcOpenShell","professional review"))
    assert report.present == len(artifacts) and report.status.startswith("LOCAL_CONTRACTS_VALID")
    assert "OCCT" in report.external_pending
