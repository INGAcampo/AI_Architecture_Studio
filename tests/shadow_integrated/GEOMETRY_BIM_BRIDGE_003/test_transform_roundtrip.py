import math

from geometry_bim_bridge.contracts import BridgeEntityRef, BridgeMesh
from geometry_bim_bridge_ext.identity import make_geometry_identity
from geometry_bim_bridge_ext.render_payload import RenderMeshPayload, canonical_mesh_sha256
from geometry_bim_bridge_xform.transform import RigidTransform, transform_mesh, transform_render_payload
from geometry_bim_bridge_xform.roundtrip import evaluate_roundtrip_identity


def test_rigid_transform_rotates_and_translates_mesh():
    mesh=BridgeMesh(
        vertices=((1.0,0.0,0.0),(0.0,1.0,0.0),(0.0,0.0,0.0)),
        triangles=((0,1,2),),
    )
    out=transform_mesh(mesh,RigidTransform(tx=10.0,ty=20.0,tz=5.0,rz_degrees=90.0))

    assert math.isclose(out.vertices[0][0],10.0,abs_tol=1e-12)
    assert math.isclose(out.vertices[0][1],21.0,abs_tol=1e-12)
    assert math.isclose(out.vertices[0][2],5.0,abs_tol=1e-12)


def test_transform_updates_bounds_and_hash():
    payload=RenderMeshPayload(
        entity_id="1",
        entity_type="Wall",
        global_id="G1",
        vertices=((0.0,0.0,0.0),(1.0,0.0,0.0),(0.0,1.0,0.0)),
        triangles=((0,1,2),),
        bounds_min=(0.0,0.0,0.0),
        bounds_max=(1.0,1.0,0.0),
        mesh_sha256="0"*64,
        metadata={},
    )
    out=transform_render_payload(payload,RigidTransform(tx=2.0,ty=3.0,tz=4.0))
    assert out.bounds_min==(2.0,3.0,4.0)
    assert out.bounds_max==(3.0,4.0,4.0)
    assert len(out.mesh_sha256)==64
    assert out.mesh_sha256!="0"*64


def test_identity_guard_detects_geometry_change():
    entity=BridgeEntityRef("AIAS","1","Wall","G1")
    m1=BridgeMesh(((0.,0.,0.),(1.,0.,0.),(0.,1.,0.)),((0,1,2),))
    m2=transform_mesh(m1,RigidTransform(tx=1.0))
    i1=make_geometry_identity(entity,canonical_mesh_sha256(m1))
    i2=make_geometry_identity(entity,canonical_mesh_sha256(m2))
    guard=evaluate_roundtrip_identity(i1,i2)
    assert guard.semantic_identity_preserved is True
    assert guard.geometry_identity_preserved is False
    assert guard.composite_identity_preserved is False
    assert guard.passed is False
