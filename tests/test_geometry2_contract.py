import json
from pathlib import Path
from aias_geometry2 import GeometryKernelAdapter, SemanticShape
ROOT = Path(__file__).resolve().parents[1]
def test_geometry2_reports_external_boundary_honestly():
    status = GeometryKernelAdapter().availability()
    assert status.native_aias is True and status.production_ready is False
def test_geometry2_validates_semantic_shape_contract():
    result = GeometryKernelAdapter().validate_semantic_shape(SemanticShape("wall-1", "solid", {"height": 3}))
    assert result["valid"] is True and result["backend"] == "aias-native-contract"
def test_geometry2_spec_keeps_occt_gates_explicit():
    spec = json.loads((ROOT / "engineering/aias/geometry/GEOMETRY_2_CONTRACT.json").read_text(encoding="utf-8"))
    assert spec["gates"]["license"] == "PENDING"
