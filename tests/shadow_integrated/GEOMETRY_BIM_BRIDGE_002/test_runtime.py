import pytest
from geometry_bim_bridge.bridge import GeometryBimBridge
from geometry_bim_bridge.ifc_adapter import create_minimal_wall_model
from geometry_bim_bridge.occt_adapter import make_box
from geometry_bim_bridge_ext.render_payload import build_render_payload

r=GeometryBimBridge.runtime()
pytestmark=pytest.mark.skipif(not(r.ifcopenshell and r.occt),reason="optional runtime")

def test_real_ifc_occt_to_render_contract():
    model,wall=create_minimal_wall_model()
    shape=make_box(2.,0.2,3.)
    p=GeometryBimBridge.from_ifc_entity_and_shape(wall,shape,linear_deflection=0.25)
    out=build_render_payload(p)
    assert out.entity_type=="IfcWall"
    assert len(out.vertices)>0 and len(out.triangles)>0
