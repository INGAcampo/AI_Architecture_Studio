import json
from pathlib import Path
from aias_bim_native2 import BimNativeAdapter, BimEntity
ROOT = Path(__file__).resolve().parents[1]
def test_ifc_gate_is_explicitly_pending():
    status=BimNativeAdapter().availability()
    assert status.native_aias is True and status.production_ready is False
def test_bim_entity_contract_is_semantic_and_deterministic():
    result=BimNativeAdapter().validate_entity(BimEntity("wall-1","IfcWall",{"Height":3}))
    assert result["valid"] is True and result["backend"] == "aias-semantic-contract"
def test_availability_evidence_matches_environment_gate():
    evidence=json.loads((ROOT/"engineering/aias/bim/BIM_NATIVE_2_001_AVAILABILITY.json").read_text(encoding="utf-8"))
    assert evidence["available"] is False and evidence["no_blocking_claim"] is True
