import pytest

from geometry_bim_bridge.bridge import GeometryBimBridge
from geometry_bim_bridge.ifc_adapter import create_minimal_wall_model
from geometry_bim_bridge.occt_adapter import make_box
from geometry_bim_bridge_ext.render_payload import build_render_payload
from geometry_bim_bridge_xform.transform import RigidTransform, transform_render_payload

runtime=GeometryBimBridge.runtime()
pytestmark=pytest.mark.skipif(
    not(runtime.ifcopenshell and runtime.occt),
    reason="optional runtime"
)

def test_real_ifc_occt_payload_can_be_transformed_without_semantic_loss():
    model,wall=create_minimal_wall_model()
    shape=make_box(2.0,0.2,3.0)
    bridge=GeometryBimBridge.from_ifc_entity_and_shape(wall,shape,linear_deflection=0.25)
    render=build_render_payload(bridge)
    moved=transform_render_payload(render,RigidTransform(tx=5.0,ty=2.0,tz=1.0,rz_degrees=15.0))
    assert moved.entity_id==render.entity_id
    assert moved.entity_type==render.entity_type
    assert moved.global_id==render.global_id
    assert moved.mesh_sha256!=render.mesh_sha256
