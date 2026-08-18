import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_all_contract_specs_are_present():
    paths=["engineering/aias/development_factory/ADF_002_DEPENDENCY_GRAPH.json","engineering/aias/geometry/GEOMETRY_2_CONTRACT.json","engineering/aias/roadmap/MEGABLOCK_BIM_NATIVE_2_SPEC.json","engineering/aias/roadmap/GEOMETRY_BIM_BRIDGE_001_SPEC.json","engineering/aias/structural_platform1/STRUCTURAL_PLATFORM_1_SPEC.json","engineering/aias/standards_engine/STANDARDS_ENGINE_001_SPEC.json","engineering/aias/aec_orchestrator/AEC_ORCHESTRATOR_001_SPEC.json","engineering/aias/engineering_agents/AI_ENGINEERING_AGENTS_001_SPEC.json"]
    assert all((ROOT/p).is_file() for p in paths)
def test_release_gate_labels_external_and_professional_boundaries():
    spec=json.loads((ROOT/"engineering/aias/release_gate/AIAS_NEXT_002_SPEC.json").read_text(encoding="utf-8"))
    assert "external_runtime_evidence" in spec["gates"]
    assert "normative compliance" in spec["claims_not_made"]
