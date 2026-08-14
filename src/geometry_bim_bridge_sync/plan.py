from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SyncAction:
    action: str
    instance_id: str


@dataclass(frozen=True)
class SyncPlan:
    actions: tuple[SyncAction,...]


def build_sync_plan(change_set) -> SyncPlan:
    actions=[]

    for instance_id in change_set.removed:
        actions.append(SyncAction("REMOVE",instance_id))

    for instance_id in change_set.added:
        actions.append(SyncAction("ADD",instance_id))

    for instance_id in change_set.geometry_changed:
        actions.append(SyncAction("UPDATE_GEOMETRY",instance_id))

    for instance_id in change_set.metadata_changed:
        if instance_id not in set(change_set.geometry_changed):
            actions.append(SyncAction("UPDATE_METADATA",instance_id))

    return SyncPlan(actions=tuple(actions))
