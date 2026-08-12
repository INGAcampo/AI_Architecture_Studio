"""Selection bridge joining project/BIM navigation, canvas and property inspection."""
from __future__ import annotations

from typing import Any, Iterable

from gui.workspace import DockArea, PanelDescriptor


def _object_id(obj: Any) -> str:
    if isinstance(obj, dict):
        value = obj.get("object_id", obj.get("id"))
    else:
        value = getattr(obj, "object_id", getattr(obj, "id", None))
    if value is None or not str(value).strip():
        raise ValueError("engineering_object_requires_stable_id")
    return str(value)


class BimInspectorCoordinator:
    """One deterministic selection path for browser, canvas and inspector."""

    def __init__(self, workspace, browser_controller, property_controller, objects: Iterable[Any] = ()) -> None:
        self.workspace = workspace
        self.browser = browser_controller
        self.properties = property_controller
        self._objects: dict[str, Any] = {}
        self._synchronizing = False
        self.refresh_objects(objects)
        # Route legacy browser selection into the same state authority.
        self.browser.workspace = workspace

    def refresh_objects(self, objects: Iterable[Any]) -> None:
        indexed: dict[str, Any] = {}
        for obj in objects:
            identifier = _object_id(obj)
            if identifier in indexed:
                raise KeyError(f"duplicate_engineering_object_id:{identifier}")
            indexed[identifier] = obj
        self._objects = indexed
        current = getattr(self.workspace.state, "selection_ids", ())
        self.synchronize(current, origin="model_refresh")

    def install_standard_panels(self) -> None:
        descriptors = (
            PanelDescriptor("project_browser", "Project / BIM", DockArea.LEFT, category="model"),
            PanelDescriptor("property_inspector", "Properties", DockArea.RIGHT, category="model"),
        )
        for descriptor in descriptors:
            if descriptor.panel_id not in self.workspace.registry:
                self.workspace.register_panel(descriptor)
            self.workspace.panels.activate(descriptor.panel_id)
        self.workspace.capture_panel_state()

    def select_from_browser(self, node_id: str | None) -> dict:
        self.browser.select_node(node_id)
        if node_id is None:
            return self.synchronize((), origin="browser")
        node = self.browser.model.require(node_id)
        return self.synchronize((node.object_id,) if node.object_id else (), origin="browser")

    def select_from_canvas(self, identifiers: Iterable[str]) -> dict:
        return self.synchronize(identifiers, origin="canvas")

    def synchronize(self, identifiers: Iterable[str], *, origin: str = "external") -> dict:
        normalized = tuple(dict.fromkeys(str(value) for value in identifiers if value is not None))
        if self._synchronizing:
            return {"selection_ids": list(normalized), "resolved": 0, "missing": [], "origin": origin}
        self._synchronizing = True
        try:
            resolved = tuple(self._objects[item] for item in normalized if item in self._objects)
            missing = tuple(item for item in normalized if item not in self._objects)
            self.workspace.set_selection(normalized)
            self.browser.handle_workspace_selection(normalized)
            if resolved:
                self.properties.set_selection(resolved)
            else:
                self.properties.clear_selection()
            result = {"selection_ids": list(normalized), "resolved": len(resolved), "missing": list(missing), "origin": origin}
            self.workspace.events.publish("workspace2.model.selection.synchronized", **result)
            return result
        finally:
            self._synchronizing = False

    def object(self, identifier: str) -> Any:
        try:
            return self._objects[str(identifier)]
        except KeyError as exc:
            raise KeyError(f"unknown_engineering_object:{identifier}") from exc
