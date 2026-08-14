from __future__ import annotations

from dataclasses import dataclass

from .filtering import VisibilityRule, matches_visibility_rule


@dataclass(frozen=True)
class SceneBatchItem:
    instance_id: str
    payload: object


@dataclass(frozen=True)
class SceneBatch:
    items: tuple[SceneBatchItem,...]
    total_vertices: int
    total_triangles: int


def build_visible_batch(
    items: tuple[SceneBatchItem,...],
    rule: VisibilityRule,
) -> SceneBatch:
    visible=[]

    for item in items:
        if not item.instance_id.strip():
            raise ValueError("instance_id must not be empty")

        if matches_visibility_rule(item.payload,rule):
            visible.append(item)

    return SceneBatch(
        items=tuple(visible),
        total_vertices=sum(len(item.payload.vertices) for item in visible),
        total_triangles=sum(len(item.payload.triangles) for item in visible),
    )
