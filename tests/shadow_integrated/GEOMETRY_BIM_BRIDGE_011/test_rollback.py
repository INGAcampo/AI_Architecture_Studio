from geometry_bim_bridge_patch_order.order import OrderedPatchOperation
from geometry_bim_bridge_rollback.rollback import build_rollback_plan

def test_add_rolls_back_as_remove():
    ordered=(OrderedPatchOperation("ADD","A",0),)
    r=build_rollback_plan(ordered,set())
    assert tuple((x.op,x.instance_id) for x in r.operations)==(("REMOVE","A"),)
    assert r.fully_reversible is True

def test_update_requires_snapshot_for_full_reversibility():
    ordered=(OrderedPatchOperation("UPDATE_GEOMETRY","A",0),)
    r=build_rollback_plan(ordered,set())
    assert r.fully_reversible is False
    r2=build_rollback_plan(ordered,{"A"})
    assert r2.fully_reversible is True

def test_rollback_order_is_reverse_of_patch_order():
    ordered=(
        OrderedPatchOperation("ADD","A",0),
        OrderedPatchOperation("UPDATE_METADATA","B",1),
    )
    r=build_rollback_plan(ordered,{"B"})
    assert tuple(x.instance_id for x in r.operations)==("B","A")
