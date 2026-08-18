import json
from pathlib import Path
import pytest
from aias_geometry_bim_bridge.tessellation import tessellate_box
ROOT=Path(__file__).resolve().parents[1]
def test_tessellation_preserves_object_identity_and_is_deterministic():
    record={"object_id":"wall-001","geometry":{"parameters":{"height":3,"length":5,"thickness":.2}}}
    first=tessellate_box(record); second=tessellate_box(record)
    assert first == second and first["object_id"] == "wall-001" and first["engineering_brep"] is False
    assert len(first["vertices"]) == 8 and len(first["triangles"]) == 12
def test_tessellation_rejects_invalid_dimensions():
    with pytest.raises(ValueError,match="positive_box_dimensions_required"): tessellate_box({"object_id":"w","geometry":{"parameters":{"height":0,"length":1,"thickness":1}}})
def test_evidence_is_honest_about_preview_scope():
    evidence=json.loads((ROOT/"engineering/aias/bridge/GEOMETRY_BIM_BRIDGE_002_EVIDENCE.json").read_text(encoding="utf-8"))
    assert "OCCT B-Rep" in evidence["not_claimed"]
