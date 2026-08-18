from geometry_bim_bridge_ext.render_payload import RenderMeshPayload
from geometry_bim_bridge_batch.batch import SceneBatchItem,build_visible_batch
from geometry_bim_bridge_batch.filtering import VisibilityRule


def payload(entity_type,global_id):
    return RenderMeshPayload(
        entity_id=global_id or "NONE",
        entity_type=entity_type,
        global_id=global_id,
        vertices=((0.,0.,0.),(1.,0.,0.),(0.,1.,0.)),
        triangles=((0,1,2),),
        bounds_min=(0.,0.,0.),
        bounds_max=(1.,1.,0.),
        mesh_sha256="0"*64,
        metadata={},
    )


def test_batch_filters_by_entity_type():
    items=(
        SceneBatchItem("A",payload("IfcWall","W")),
        SceneBatchItem("B",payload("IfcSlab","S")),
    )

    batch=build_visible_batch(
        items,
        VisibilityRule(entity_types=("IfcWall",)),
    )

    assert len(batch.items)==1
    assert batch.items[0].payload.entity_type=="IfcWall"
    assert batch.total_vertices==3
    assert batch.total_triangles==1


def test_batch_filters_by_global_id():
    items=(
        SceneBatchItem("A",payload("IfcWall","W1")),
        SceneBatchItem("B",payload("IfcWall","W2")),
    )

    batch=build_visible_batch(
        items,
        VisibilityRule(global_ids=("W2",)),
    )

    assert len(batch.items)==1
    assert batch.items[0].payload.global_id=="W2"


def test_hidden_rule_returns_empty_batch():
    items=(SceneBatchItem("A",payload("IfcWall","W")),)
    batch=build_visible_batch(items,VisibilityRule(hidden=True))
    assert batch.items==()
    assert batch.total_vertices==0
