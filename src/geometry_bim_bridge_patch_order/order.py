from __future__ import annotations
from dataclasses import dataclass

_PRIORITY={
    "REMOVE":0,
    "ADD":1,
    "UPDATE_GEOMETRY":2,
    "UPDATE_METADATA":3,
}

@dataclass(frozen=True)
class OrderedPatchOperation:
    op:str
    instance_id:str
    order_index:int

def order_patch_operations(operations):
    values=tuple(operations)
    for item in values:
        if item.op not in _PRIORITY:
            raise ValueError("unsupported patch operation")
        if not item.instance_id.strip():
            raise ValueError("instance_id must not be empty")

    ordered=sorted(
        values,
        key=lambda item:(_PRIORITY[item.op],item.instance_id),
    )

    return tuple(
        OrderedPatchOperation(item.op,item.instance_id,index)
        for index,item in enumerate(ordered)
    )
