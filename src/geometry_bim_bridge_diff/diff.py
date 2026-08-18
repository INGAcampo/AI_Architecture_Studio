from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SceneItemSignature:
    instance_id: str
    semantic_global_id: str | None
    mesh_sha256: str
    metadata_sha256: str

    def validate(self) -> None:
        if not self.instance_id.strip():
            raise ValueError("instance_id must not be empty")
        if len(self.mesh_sha256) != 64:
            raise ValueError("mesh_sha256 must be SHA256")
        if len(self.metadata_sha256) != 64:
            raise ValueError("metadata_sha256 must be SHA256")


@dataclass(frozen=True)
class SceneChangeSet:
    added: tuple[str,...]
    removed: tuple[str,...]
    geometry_changed: tuple[str,...]
    metadata_changed: tuple[str,...]
    unchanged: tuple[str,...]


def diff_scene_signatures(before, after) -> SceneChangeSet:
    left={}
    right={}

    for item in before:
        item.validate()
        if item.instance_id in left:
            raise ValueError("duplicate instance_id in before")
        left[item.instance_id]=item

    for item in after:
        item.validate()
        if item.instance_id in right:
            raise ValueError("duplicate instance_id in after")
        right[item.instance_id]=item

    left_ids=set(left)
    right_ids=set(right)

    added=sorted(right_ids-left_ids)
    removed=sorted(left_ids-right_ids)
    geometry_changed=[]
    metadata_changed=[]
    unchanged=[]

    for instance_id in sorted(left_ids & right_ids):
        a=left[instance_id]
        b=right[instance_id]

        geometry_diff=a.mesh_sha256 != b.mesh_sha256
        metadata_diff=a.metadata_sha256 != b.metadata_sha256

        if geometry_diff:
            geometry_changed.append(instance_id)
        if metadata_diff:
            metadata_changed.append(instance_id)
        if not geometry_diff and not metadata_diff:
            unchanged.append(instance_id)

    return SceneChangeSet(
        added=tuple(added),
        removed=tuple(removed),
        geometry_changed=tuple(geometry_changed),
        metadata_changed=tuple(metadata_changed),
        unchanged=tuple(unchanged),
    )
