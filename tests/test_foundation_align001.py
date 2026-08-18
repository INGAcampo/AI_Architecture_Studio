import json
from pathlib import Path
from aias_foundation_governance.hierarchy import governing_authority
from aias_foundation_governance.orchestrator import FoundationGovernanceOrchestrator
from aias_foundation_governance.validator import FoundationValidator
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/"engineering"/"aias"/"foundation"/name).read_text(encoding="utf-8"))
def test_charter_is_complete_and_acceleration_is_constitutional():assert FoundationValidator().validate_charter(load("AIAS_CHARTER.json"))==[]
def test_handbook_dependency_direction_is_valid():assert FoundationValidator().validate_handbook(load("AIAS_ARCHITECTURE_HANDBOOK.json"))==[]
def test_charter_governs_generated_evidence():assert governing_authority("AIAS Charter","Generated Evidence")=="AIAS Charter"
def test_forbidden_upward_dependency_is_rejected():
 h=load("AIAS_ARCHITECTURE_HANDBOOK.json");c={k:[] for k in h["component_contract_required_fields"]};c.update({"layer":"L1","dependency_layers":["L5"]});assert "forbidden_dependency:L1->L5" in FoundationValidator().validate_component(c,h)
def test_complete_contract_is_accepted():
 h=load("AIAS_ARCHITECTURE_HANDBOOK.json");c={k:[] for k in h["component_contract_required_fields"]};c.update({"layer":"L3","dependency_layers":["L0","L2"]});assert FoundationValidator().validate_component(c,h)==[]
def test_orchestrator_builds_release(tmp_path):
 r=FoundationGovernanceOrchestrator().execute(ROOT,tmp_path);assert r["validated"] and r["layers"]==6 and Path(r["archive"]).is_file() and len(r["sha256"])==64
