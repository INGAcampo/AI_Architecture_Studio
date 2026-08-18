import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_external_registry_has_all_required_authority_domains():
    registry=json.loads((ROOT/"engineering/aias/external_gates/AIAS_NEXT_004_EXTERNAL_GATE_REGISTRY.json").read_text(encoding="utf-8"))
    subjects=" ".join(item["subject"] for item in registry["entries"])
    assert all(term in subjects for term in ("OCCT","IfcOpenShell","Venezuelan","AutoCAD","Independent"))
def test_registry_never_infers_missing_evidence():
    registry=json.loads((ROOT/"engineering/aias/external_gates/AIAS_NEXT_004_EXTERNAL_GATE_REGISTRY.json").read_text(encoding="utf-8"))
    assert "missing evidence is never inferred" in registry["rules"]
    assert all(item["evidence_status"] != "VERIFIED" for item in registry["entries"])
