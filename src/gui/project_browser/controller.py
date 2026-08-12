from __future__ import annotations

from typing import Iterable

from .model import ProjectBrowserModel
from .state import ProjectBrowserState


class ProjectBrowserController:
    def __init__(
        self,
        model: ProjectBrowserModel,
        *,
        workspace=None,
        event_dispatcher=None,
    ) -> None:
        self.model = model
        self.workspace = workspace
        self.event_dispatcher = event_dispatcher
        self.state = ProjectBrowserState()

    def set_filter(self, text: str):
        normalized = text.strip()
        self.state.filter_text = normalized
        return self.model.filter(normalized)

    def select_node(self, node_id: str | None) -> None:
        if node_id is None:
            self.state.selected_node_id = None
            self._push_workspace_selection(())
            return

        node = self.model.require(node_id)
        self.state.selected_node_id = node_id
        if node.object_id:
            self._push_workspace_selection((node.object_id,))

    def select_object(self, object_id: str) -> str | None:
        node = self.model.find_by_object_id(object_id)
        if node is None:
            return None
        self.state.selected_node_id = node.node_id
        return node.node_id

    def set_expanded(self, node_id: str, expanded: bool) -> None:
        self.model.require(node_id)
        if expanded:
            self.state.expanded_node_ids.add(node_id)
        else:
            self.state.expanded_node_ids.discard(node_id)

    def refresh(self, new_model: ProjectBrowserModel) -> None:
        selected_object_id = None
        if self.state.selected_node_id:
            previous = self.model.require(self.state.selected_node_id)
            selected_object_id = previous.object_id

        valid_expanded = {
            node_id
            for node_id in self.state.expanded_node_ids
            if node_id in new_model.snapshot()["nodes"]
        }
        self.model = new_model
        self.state.expanded_node_ids = valid_expanded

        if selected_object_id:
            found = new_model.find_by_object_id(selected_object_id)
            self.state.selected_node_id = found.node_id if found else None
        elif self.state.selected_node_id not in new_model.snapshot()["nodes"]:
            self.state.selected_node_id = None

        self._publish("project_browser.refreshed", revision=new_model.revision)

    def handle_workspace_selection(self, identifiers: Iterable[str]) -> str | None:
        first = next(iter(identifiers), None)
        if first is None:
            self.state.selected_node_id = None
            return None
        return self.select_object(str(first))

    def _push_workspace_selection(self, identifiers: tuple[str, ...]) -> None:
        workspace = self.workspace
        setter = getattr(workspace, "set_selection", None)
        if callable(setter):
            setter(identifiers)
        self._publish(
            "project_browser.selection.changed",
            selection_ids=identifiers,
        )

    def _publish(self, name: str, **payload) -> None:
        target = self.event_dispatcher
        if target is None:
            return
        dispatch = getattr(target, "dispatch", None)
        if callable(dispatch):
            try:
                dispatch(name, payload)
            except TypeError:
                dispatch({"name": name, "payload": payload})
            return
        if callable(target):
            target(name, payload)
