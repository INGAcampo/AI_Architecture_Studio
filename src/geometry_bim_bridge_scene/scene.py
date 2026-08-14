from __future__ import annotations

from dataclasses import dataclass

from geometry_bim_bridge_xform.transform import RigidTransform, transform_render_payload


@dataclass(frozen=True)
class SceneTransformChain:
    transforms: tuple[RigidTransform, ...] = ()


@dataclass(frozen=True)
class SceneInstance:
    instance_id: str
    semantic_global_id: str | None
    payload: object
    transform_chain: SceneTransformChain

    def validate(self) -> None:
        if not self.instance_id.strip():
            raise ValueError("instance_id must not be empty")


def apply_transform_chain(instance: SceneInstance):
    instance.validate()
    payload=instance.payload

    for transform in instance.transform_chain.transforms:
        payload=transform_render_payload(payload,transform)

    return payload
