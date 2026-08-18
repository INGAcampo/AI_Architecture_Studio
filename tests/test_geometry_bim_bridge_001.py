import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_bridge_owns_convergence_without_merging_kernels():
    spec=json.loads((ROOT/"engineering/aias/roadmap/GEOMETRY_BIM_BRIDGE_001_SPEC.json").read_text(encoding="utf-8"))
    assert spec["ownership"]["bim"] == "MEGABLOCK-BIM-NATIVE-2"
    assert spec["ownership"]["geometry"] == "MEGABLOCK-GEOMETRY-2.0-A"
    assert "stable AIAS object ID survives round trip" in spec["invariants"]
def test_bridge_keeps_external_gates_explicit():
    spec=json.loads((ROOT/"engineering/aias/roadmap/GEOMETRY_BIM_BRIDGE_001_SPEC.json").read_text(encoding="utf-8"))
    assert "external runtime availability" in spec["gates"]
    assert "production IFC round trip" in spec["status_claims_not_made"]
