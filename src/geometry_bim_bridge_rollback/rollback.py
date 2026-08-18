from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RollbackOperation:
    op:str
    instance_id:str

@dataclass(frozen=True)
class RollbackPlan:
    operations:tuple[RollbackOperation,...]
    fully_reversible:bool

_INVERSE={
    "ADD":"REMOVE",
    "REMOVE":"RESTORE",
    "UPDATE_GEOMETRY":"RESTORE_GEOMETRY",
    "UPDATE_METADATA":"RESTORE_METADATA",
}

def build_rollback_plan(ordered_operations, snapshots_available:set[str])->RollbackPlan:
    rollback=[]
    fully=True

    for item in reversed(tuple(ordered_operations)):
        inverse=_INVERSE.get(item.op)
        if inverse is None:
            raise ValueError("unsupported patch operation")

        if inverse.startswith("RESTORE") and item.instance_id not in snapshots_available:
            fully=False

        rollback.append(RollbackOperation(inverse,item.instance_id))

    return RollbackPlan(tuple(rollback),fully)
