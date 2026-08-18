from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable

from aias_i18n import tr


class BrowserNodeKind(str, Enum):
    ROOT = "root"
    GROUP = "group"
    LEVEL = "level"
    CATEGORY = "category"
    OBJECT = "object"
    MATERIAL = "material"


@dataclass(slots=True)
class BrowserNode:
    node_id: str
    title: str
    kind: BrowserNodeKind
    parent_id: str | None = None
    object_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    children: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise ValueError(tr("error.empty_node_id"))
        if not self.title.strip():
            raise ValueError(tr("error.empty_title"))

    def snapshot(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "title": self.title,
            "kind": self.kind.value,
            "parent_id": self.parent_id,
            "object_id": self.object_id,
            "metadata": dict(self.metadata),
            "children": list(self.children),
        }


class ProjectBrowserModel:
    ROOT_ID = "project"

    def __init__(self, title: str = "Proyecto") -> None:
        self._nodes: dict[str, BrowserNode] = {
            self.ROOT_ID: BrowserNode(
                node_id=self.ROOT_ID,
                title=title,
                kind=BrowserNodeKind.ROOT,
            )
        }
        self.revision = 0

    def _touch(self) -> int:
        self.revision += 1
        return self.revision

    def add_node(self, node: BrowserNode) -> BrowserNode:
        if node.node_id in self._nodes:
            raise KeyError(tr("browser.error_duplicate_node", node_id=node.node_id))
        parent_id = node.parent_id or self.ROOT_ID
        parent = self.require(parent_id)
        node.parent_id = parent_id
        self._nodes[node.node_id] = node
        parent.children.append(node.node_id)
        self._touch()
        return node

    def upsert_node(self, node: BrowserNode) -> BrowserNode:
        current = self._nodes.get(node.node_id)
        if current is None:
            return self.add_node(node)

        changed = (
            current.title != node.title
            or current.kind != node.kind
            or current.object_id != node.object_id
            or current.metadata != node.metadata
        )
        if changed:
            current.title = node.title
            current.kind = node.kind
            current.object_id = node.object_id
            current.metadata = dict(node.metadata)
            self._touch()
        return current

    def remove_node(self, node_id: str) -> tuple[str, ...]:
        if node_id == self.ROOT_ID:
            raise ValueError(tr("browser.error_delete_root"))
        node = self.require(node_id)
        removed: list[str] = []

        def remove_recursive(current_id: str) -> None:
            current = self.require(current_id)
            for child_id in tuple(current.children):
                remove_recursive(child_id)
            self._nodes.pop(current_id)
            removed.append(current_id)

        parent = self.require(node.parent_id or self.ROOT_ID)
        parent.children.remove(node_id)
        remove_recursive(node_id)
        self._touch()
        return tuple(removed)

    def move_node(self, node_id: str, new_parent_id: str) -> None:
        if node_id == self.ROOT_ID:
            raise ValueError(tr("browser.error_move_root"))
        node = self.require(node_id)
        new_parent = self.require(new_parent_id)

        ancestor = new_parent
        while ancestor.parent_id is not None:
            if ancestor.node_id == node_id:
                raise ValueError(tr("browser.error_move_self"))
            ancestor = self.require(ancestor.parent_id)

        old_parent = self.require(node.parent_id or self.ROOT_ID)
        if old_parent.node_id == new_parent.node_id:
            return
        old_parent.children.remove(node_id)
        new_parent.children.append(node_id)
        node.parent_id = new_parent_id
        self._touch()

    def require(self, node_id: str) -> BrowserNode:
        try:
            return self._nodes[node_id]
        except KeyError as exc:
            raise KeyError(tr("browser.error_unknown_node", node_id=node_id)) from exc

    def find_by_object_id(self, object_id: str) -> BrowserNode | None:
        return next(
            (node for node in self._nodes.values() if node.object_id == object_id),
            None,
        )

    def children_of(self, node_id: str) -> tuple[BrowserNode, ...]:
        node = self.require(node_id)
        return tuple(self.require(child_id) for child_id in node.children)

    def iter_depth_first(self, node_id: str = ROOT_ID) -> Iterable[BrowserNode]:
        node = self.require(node_id)
        yield node
        for child_id in node.children:
            yield from self.iter_depth_first(child_id)

    def filter(self, query: str) -> tuple[BrowserNode, ...]:
        text = query.strip().casefold()
        if not text:
            return tuple(self.iter_depth_first())
        return tuple(
            node for node in self.iter_depth_first()
            if text in node.title.casefold()
            or text in (node.object_id or "").casefold()
            or any(text in str(value).casefold() for value in node.metadata.values())
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "revision": self.revision,
            "root_id": self.ROOT_ID,
            "nodes": {
                node_id: node.snapshot()
                for node_id, node in sorted(self._nodes.items())
            },
        }
