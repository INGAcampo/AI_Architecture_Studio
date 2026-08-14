from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class PatchOperation:
    op:str
    instance_id:str

@dataclass(frozen=True)
class PatchPlan:
    operations:tuple[PatchOperation,...]
    destructive:bool

def compile_patch_plan(sync_plan)->PatchPlan:
    ops=[]
    destructive=False
    for action in sync_plan.actions:
        if action.action=="REMOVE":
            destructive=True
        if action.action not in {"REMOVE","ADD","UPDATE_GEOMETRY","UPDATE_METADATA"}:
            raise ValueError("unsupported sync action")
        ops.append(PatchOperation(action.action,action.instance_id))
    return PatchPlan(tuple(ops),destructive)
