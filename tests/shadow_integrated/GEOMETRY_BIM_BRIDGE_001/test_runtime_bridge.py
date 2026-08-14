import pytest

from geometry_bim_bridge.bridge import GeometryBimBridge
from geometry_bim_bridge.ifc_adapter import create_minimal_wall_model
from geometry_bim_bridge.occt_adapter import make_box


runtime = GeometryBimBridge.runtime()
pytestmark = pytest.mark.skipif(
    not (runtime.ifcopenshell and runtime.occt),
    reason="IfcOpenShell and OCP/OCCT are optional and validated in an isolated runtime.",
)


def test_ifc_entity_plus_occt_shape_to_bridge_payload():
    model, wall = create_minimal_wall_model()
    shape = make_box(2.0, 0.2, 3.0)

    payload = GeometryBimBridge.from_ifc_entity_and_shape(
        wall,
        shape,
        linear_deflection=0.25,
        metadata={"source": "shadow-golden"},
    )

    assert payload.entity.source == "IFC"
    assert payload.entity.entity_type == "IfcWall"
    assert payload.entity.global_id == wall.GlobalId
    assert payload.geometry_kind == "OCCT_BREP"
    assert payload.topology.solids >= 1
    assert payload.topology.faces >= 6
    assert payload.mesh is not None
    assert len(payload.mesh.vertices) > 0
    assert len(payload.mesh.triangles) > 0
    assert payload.metadata["source"] == "shadow-golden"


def test_aias_semantic_ref_plus_occt_shape_to_bridge_payload():
    shape = make_box(1.0, 1.0, 1.0)

    payload = GeometryBimBridge.from_aias_semantic_ref_and_shape(
        "AIAS-WALL-001",
        "Wall",
        shape,
        global_id="AIAS-GID-001",
        linear_deflection=0.25,
    )

    assert payload.entity.source == "AIAS"
    assert payload.entity.entity_id == "AIAS-WALL-001"
    assert payload.entity.global_id == "AIAS-GID-001"
    assert payload.topology.solids >= 1
    assert payload.mesh is not None
