import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_geometry_2_0_a_owns_math_and_excludes_bim_responsibility():
    spec = json.loads((ROOT / "engineering/aias/roadmap/MEGABLOCK_GEOMETRY_2_0_A_SPEC.json").read_text(encoding="utf-8"))
    assert spec["primary_backend"] == "OCCT/Open CASCADE"
    assert "IFC entity semantics" in spec["non_responsibilities"]
    assert "runtime availability" in spec["gates"]
def test_geometry_2_0_a_does_not_claim_unverified_installation():
    spec = json.loads((ROOT / "engineering/aias/roadmap/MEGABLOCK_GEOMETRY_2_0_A_SPEC.json").read_text(encoding="utf-8"))
    assert "OCCT installed" in spec["claims_not_made"]
    assert spec["status"] == "FORMALLY_ACTIVATED_CONTRACT_PHASE"
