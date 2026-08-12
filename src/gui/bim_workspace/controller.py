from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .builder import BimWorkspaceBuilder
from .catalogs import FamilyCatalog, MaterialCatalog
from .entities import BimWorkspaceNodeKind
from .tree import BimWorkspaceTree


@dataclass(slots=True)
class BimWorkspaceState:
    selected_node_id: str | None = None
    expanded_node_ids: set[str] = field(default_factory=set)
    query: str = ""
    kind_filter: set[BimWorkspaceNodeKind] = field(default_factory=set)

    def snapshot(self) -> dict:
        return {
            "selected_node_id": self.selected_node_id,
            "expanded_node_ids": sorted(self.expanded_node_ids),
            "query": self.query,
            "kind_filter": sorted(kind.value for kind in self.kind_filter),
        }


class BimWorkspaceController:
    def __init__(
        self,
        tree: BimWorkspaceTree,
        *,
        workspace=None,
        event_dispatcher=None,
    ) -> None:
        self.tree = tree
        self.workspace = workspace
        self.event_dispatcher = event_dispatcher
        self.state = BimWorkspaceState()

    def select_node(self, node_id: str | None) -> None:
        if node_id is None:
            self.state.selected_node_id = None
            self._set_workspace_selection(())
            return
        node = self.tree.require(node_id)
        self.state.selected_node_id = node_id
        if node.object_id:
            self._set_workspace_selection((node.object_id,))
        self._publish("bim_workspace.selection.changed", node_id=node_id)

    def select_object(self, object_id: str) -> str | None:
        node = self.tree.find_by_object_id(object_id)
        if node is None:
            return None
        self.state.selected_node_id = node.node_id
        return node.node_id

    def set_expanded(self, node_id: str, expanded: bool) -> None:
        self.tree.require(node_id)
        if expanded:
            self.state.expanded_node_ids.add(node_id)
        else:
            self.state.expanded_node_ids.discard(node_id)

    def set_filter(
        self,
        query: str = "",
        kinds: Iterable[BimWorkspaceNodeKind] | None = None,
    ):
        self.state.query = query.strip()
        self.state.kind_filter = set(kinds or ())
        return self.tree.filter(
            self.state.query,
            kinds=self.state.kind_filter,
        )

    def refresh(self, new_tree: BimWorkspaceTree) -> None:
        selected_object_id = None
        if self.state.selected_node_id:
            try:
                selected_object_id = self.tree.require(
                    self.state.selected_node_id
                ).object_id
            except KeyError:
                selected_object_id = None

        new_ids = set(new_tree.snapshot()["nodes"])
        self.state.expanded_node_ids.intersection_update(new_ids)
        self.tree = new_tree

        if selected_object_id:
            node = new_tree.find_by_object_id(selected_object_id)
            self.state.selected_node_id = node.node_id if node else None
        elif self.state.selected_node_id not in new_ids:
            self.state.selected_node_id = None

        self._publish("bim_workspace.refreshed", revision=new_tree.revision)

    def handle_workspace_selection(self, identifiers: Iterable[str]) -> str | None:
        first = next(iter(identifiers), None)
        if first is None:
            self.state.selected_node_id = None
            return None
        return self.select_object(str(first))

    def _set_workspace_selection(self, identifiers: tuple[str, ...]) -> None:
        setter = getattr(self.workspace, "set_selection", None)
        if callable(setter):
            setter(identifiers)

    def _publish(self, name: str, **payload) -> None:
        target = self.event_dispatcher
        if target is None:
            return
        if callable(target):
            target(name, payload)
            return
        dispatch = getattr(target, "dispatch", None)
        if callable(dispatch):
            try:
                dispatch(name, payload)
            except TypeError:
                dispatch({"name": name, "payload": payload})
