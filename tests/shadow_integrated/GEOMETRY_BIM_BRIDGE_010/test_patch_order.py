from geometry_bim_bridge_patch.patch import PatchOperation
from geometry_bim_bridge_patch_order.order import order_patch_operations

def test_patch_order_is_deterministic():
    result=order_patch_operations(
        (
            PatchOperation("UPDATE_METADATA","B"),
            PatchOperation("ADD","A"),
            PatchOperation("REMOVE","Z"),
            PatchOperation("UPDATE_GEOMETRY","C"),
        )
    )
    assert tuple(x.op for x in result)==(
        "REMOVE",
        "ADD",
        "UPDATE_GEOMETRY",
        "UPDATE_METADATA",
    )
    assert tuple(x.order_index for x in result)==(0,1,2,3)

def test_same_operation_orders_by_instance_id():
    result=order_patch_operations(
        (
            PatchOperation("ADD","B"),
            PatchOperation("ADD","A"),
        )
    )
    assert tuple(x.instance_id for x in result)==("A","B")
