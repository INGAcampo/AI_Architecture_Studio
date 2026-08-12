import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_bim_native_separates_ifc_semantics_from_geometry_kernel():
    spec=json.loads((ROOT/"engineering/aias/roadmap/MEGABLOCK_BIM_NATIVE_2_SPEC.json").read_text(encoding="utf-8"))
    assert spec["primary_backend"] == "IfcOpenShell adapter"
    assert "mathematical B-Rep kernel" in spec["non_responsibilities"]
    assert "Geometry-BIM Bridge contract" in spec["gates"]
