from geometry_bim_bridge.contracts import BridgeEntityRef,BridgeGeometryPayload,BridgeMesh,BridgeTopologySummary
from geometry_bim_bridge_ext.render_payload import build_render_payload,canonical_mesh_sha256
from geometry_bim_bridge_ext.identity import make_geometry_identity

def payload():
    m=BridgeMesh(((0.,0.,0.),(2.,0.,0.),(0.,3.,0.),(0.,0.,4.)),((0,1,2),(0,1,3)))
    return BridgeGeometryPayload(BridgeEntityRef("AIAS","W1","Wall","G1"),"OCCT_BREP",BridgeTopologySummary(faces=2),m,None,{"d":"arch"})

def test_renderer_neutral_payload():
    r=build_render_payload(payload())
    assert r.bounds_min==(0.,0.,0.)
    assert r.bounds_max==(2.,3.,4.)
    assert len(r.mesh_sha256)==64

def test_identity_is_stable():
    p=payload()
    h=canonical_mesh_sha256(p.mesh)
    a=make_geometry_identity(p.entity,h)
    b=make_geometry_identity(p.entity,h)
    assert a==b
    assert len(a.composite_key)==64
