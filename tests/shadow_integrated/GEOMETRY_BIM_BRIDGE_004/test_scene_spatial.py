import math

from geometry_bim_bridge_ext.render_payload import RenderMeshPayload
from geometry_bim_bridge_xform.transform import RigidTransform
from geometry_bim_bridge_scene.scene import (
    SceneInstance,
    SceneTransformChain,
    apply_transform_chain,
)
from geometry_bim_bridge_scene.spatial import SpatialPlacement, compose_placements


def make_payload():
    return RenderMeshPayload(
        entity_id="1",
        entity_type="IfcWall",
        global_id="G1",
        vertices=((0.0,0.0,0.0),(1.0,0.0,0.0),(0.0,1.0,0.0)),
        triangles=((0,1,2),),
        bounds_min=(0.0,0.0,0.0),
        bounds_max=(1.0,1.0,0.0),
        mesh_sha256="0"*64,
        metadata={},
    )


def test_scene_transform_chain_is_deterministic():
    instance=SceneInstance(
        instance_id="inst-1",
        semantic_global_id="G1",
        payload=make_payload(),
        transform_chain=SceneTransformChain(
            transforms=(
                RigidTransform(tx=2.0),
                RigidTransform(ty=3.0),
                RigidTransform(tz=4.0),
            )
        ),
    )
    result=apply_transform_chain(instance)

    assert result.bounds_min==(2.0,3.0,4.0)
    assert result.bounds_max==(3.0,4.0,4.0)


def test_nested_spatial_placement_composes_parent_rotation():
    parent=SpatialPlacement(x_m=10.0,y_m=20.0,rz_degrees=90.0)
    child=SpatialPlacement(x_m=2.0,y_m=0.0,z_m=3.0,rz_degrees=15.0)
    result=compose_placements(parent,child)

    assert math.isclose(result.tx,10.0,abs_tol=1e-12)
    assert math.isclose(result.ty,22.0,abs_tol=1e-12)
    assert math.isclose(result.tz,3.0,abs_tol=1e-12)
    assert math.isclose(result.rz_degrees,105.0,abs_tol=1e-12)


def test_blank_scene_instance_fails_closed():
    failed=False
    try:
        SceneInstance("",None,make_payload(),SceneTransformChain()).validate()
    except ValueError:
        failed=True
    assert failed is True
