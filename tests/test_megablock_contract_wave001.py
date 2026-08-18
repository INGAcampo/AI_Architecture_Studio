import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_parallel_megablock_contracts_are_complete_and_distinct():
    spec = json.loads((ROOT / "engineering/aias/roadmap/MEGABLOCK_CONTRACT_WAVE_001.json").read_text(encoding="utf-8"))
    packages = spec["parallel_packages"]
    assert {p["id"] for p in packages} == {"MEGABLOCK-GEOMETRY-2", "MEGABLOCK-BIM-NATIVE-2", "MEGABLOCK-STRUCTURAL-1"}
    assert all(p["owner"] and p["boundary"] and p["gates"] for p in packages)
    assert spec["external_evidence_required"] is True
def test_wave_does_not_claim_unverified_external_capabilities():
    spec = json.loads((ROOT / "engineering/aias/roadmap/MEGABLOCK_CONTRACT_WAVE_001.json").read_text(encoding="utf-8"))
    assert "normative compliance" in spec["claims_not_made"]
    assert "production-grade OCCT/IfcOpenShell integration" in spec["claims_not_made"]
