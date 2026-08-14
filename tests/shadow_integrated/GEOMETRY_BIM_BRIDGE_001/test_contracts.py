from geometry_bim_bridge.contracts import (
    BridgeEntityRef,
    BridgeMesh,
    BridgeTopologySummary,
)


def test_entity_ref_is_deterministic():
    ref = BridgeEntityRef(
        source="AIAS",
        entity_id="42",
        entity_type="Wall",
        global_id="gid-42",
    )
    assert ref.source == "AIAS"
    assert ref.entity_id == "42"
    assert ref.entity_type == "Wall"
    assert ref.global_id == "gid-42"


def test_mesh_validation_accepts_valid_triangle():
    mesh = BridgeMesh(
        vertices=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        triangles=((0, 1, 2),),
    )
    mesh.validate()


def test_mesh_validation_rejects_invalid_index():
    mesh = BridgeMesh(
        vertices=((0.0, 0.0, 0.0),),
        triangles=((0, 1, 2),),
    )
    failed = False
    try:
        mesh.validate()
    except ValueError:
        failed = True
    assert failed is True


def test_topology_summary_defaults_to_zero():
    summary = BridgeTopologySummary()
    assert summary.solids == 0
    assert summary.faces == 0
    assert summary.edges == 0
