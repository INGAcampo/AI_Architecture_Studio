from __future__ import annotations

from typing import Iterable

from .entities import BimWorkspaceNode, BimWorkspaceNodeKind


class BimWorkspaceTree:
    ROOT_ID = "bim_workspace"

    def __init__(self, title: str = "BIM Workspace") -> None:
        self._nodes: dict[str, BimWorkspaceNode] = {
            self.ROOT_ID: BimWorkspaceNode(
                self.ROOT_ID,
                title,
                BimWorkspaceNodeKind.ROOT,
            )
        }
        self.revision = 0

    def _touch(self) -> int:
        self.revision += 1
        return self.revision

    def add(self, node: BimWorkspaceNode) -> BimWorkspaceNode:
        if node.node_id in self._nodes:
            raise KeyError(f"Nodo ya existente: {node.node_id}")
        parent_id = node.parent_id or self.ROOT_ID
        parent = self.require(parent_id)
        node.parent_id = parent_id
        self._nodes[node.node_id] = node
        parent.children.append(node.node_id)
        self._touch()
        return node

    def require(self, node_id: str) -> BimWorkspaceNode:
        try:
            return self._nodes[node_id]
        except KeyError as exc:
            raise KeyError(f"Nodo desconocido: {node_id}") from exc

    def remove(self, node_id: str) -> tuple[str, ...]:
        if node_id == self.ROOT_ID:
            raise ValueError("No se puede eliminar la raíz")
        node = self.require(node_id)
        parent = self.require(node.parent_id or self.ROOT_ID)
        parent.children.remove(node_id)

        removed: list[str] = []
        def walk(current_id: str) -> None:
            current = self.require(current_id)
            for child_id in tuple(current.children):
                walk(child_id)
            self._nodes.pop(current_id)
            removed.append(current_id)

        walk(node_id)
        self._touch()
        return tuple(removed)

    def children_of(self, node_id: str) -> tuple[BimWorkspaceNode, ...]:
        node = self.require(node_id)
        return tuple(self.require(child_id) for child_id in node.children)

    def iter_depth_first(self, node_id: str = ROOT_ID):
        node = self.require(node_id)
        yield node
        for child_id in node.children:
            yield from self.iter_depth_first(child_id)

    def find_by_object_id(self, object_id: str) -> BimWorkspaceNode | None:
        return next(
            (node for node in self._nodes.values() if node.object_id == object_id),
            None,
        )

    def filter(
        self,
        query: str = "",
        *,
        kinds: Iterable[BimWorkspaceNodeKind] | None = None,
        metadata: dict[str, object] | None = None,
    ) -> tuple[BimWorkspaceNode, ...]:
        text = query.strip().casefold()
        kind_set = set(kinds or ())
        metadata = metadata or {}
        result = []
        for node in self.iter_depth_first():
            if kind_set and node.kind not in kind_set:
                continue
            if text and not (
                text in node.title.casefold()
                or text in (node.object_id or "").casefold()
                or any(text in str(value).casefold() for value in node.metadata.values())
            ):
                continue
            if any(node.metadata.get(key) != value for key, value in metadata.items()):
                continue
            result.append(node)
        return tuple(result)

    def snapshot(self) -> dict:
        return {
            "revision": self.revision,
            "root_id": self.ROOT_ID,
            "nodes": {
                node_id: node.snapshot()
                for node_id, node in sorted(self._nodes.items())
            },
        }
