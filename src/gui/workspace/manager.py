from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .events import WorkspaceEventSink
from .layout import LayoutManager
from .model import DocumentSession, PanelDescriptor, WorkspaceState
from .panels import DockManager, PanelManager, PanelRegistry


class WorkspaceManager:
    def __init__(
        self,
        layout_directory: str | Path,
        *,
        event_dispatcher=None,
        graph=None,
    ) -> None:
        self.registry = PanelRegistry()
        self.panels = PanelManager(self.registry)
        self.docks = DockManager(self.panels)
        self.layouts = LayoutManager(layout_directory)
        self.state = WorkspaceState()
        self.events = WorkspaceEventSink(event_dispatcher)
        self.graph = graph

    def _changed(self, event_name: str, **payload) -> None:
        revision = self.state.touch()
        payload["revision"] = revision
        self.events.publish(event_name, **payload)
        graph = self.graph
        if graph is not None:
            setter = getattr(graph, "set_value", None)
            if callable(setter):
                try:
                    setter("workspace.revision", revision)
                except (KeyError, ValueError, TypeError):
                    pass

    def register_panel(self, descriptor: PanelDescriptor) -> None:
        self.registry.register(descriptor)
        self._changed("workspace.panel.registered", panel_id=descriptor.panel_id)

    def register_panels(self, descriptors: Iterable[PanelDescriptor]) -> None:
        for descriptor in descriptors:
            self.register_panel(descriptor)

    def open_document(
        self,
        path: str | None = None,
        *,
        title: str = "Sin título",
        metadata: dict | None = None,
    ) -> DocumentSession:
        document = DocumentSession(path=path, title=title, metadata=dict(metadata or {}))
        self.state.documents[document.document_id] = document
        self.state.active_document_id = document.document_id
        self._changed("workspace.document.opened", document_id=document.document_id)
        return document

    def close_document(self, document_id: str, *, force: bool = False) -> DocumentSession:
        document = self.require_document(document_id)
        if document.modified and not force:
            raise RuntimeError("El documento contiene cambios sin guardar")
        self.state.documents.pop(document_id)
        if self.state.active_document_id == document_id:
            self.state.active_document_id = next(iter(self.state.documents), None)
        self._changed("workspace.document.closed", document_id=document_id)
        return document

    def activate_document(self, document_id: str) -> DocumentSession:
        document = self.require_document(document_id)
        if self.state.active_document_id != document_id:
            self.state.active_document_id = document_id
            self._changed("workspace.document.activated", document_id=document_id)
        return document

    def require_document(self, document_id: str) -> DocumentSession:
        try:
            return self.state.documents[document_id]
        except KeyError as exc:
            raise KeyError(f"Documento desconocido: {document_id}") from exc

    @property
    def active_document(self) -> DocumentSession | None:
        identifier = self.state.active_document_id
        return self.state.documents.get(identifier) if identifier else None

    def set_active_tool(self, tool_id: str | None) -> None:
        if self.state.active_tool != tool_id:
            self.state.active_tool = tool_id
            self._changed("workspace.tool.changed", tool_id=tool_id)

    def set_selection(self, identifiers: Iterable[str]) -> None:
        normalized = tuple(dict.fromkeys(str(item) for item in identifiers))
        if self.state.selection_ids != normalized:
            self.state.selection_ids = normalized
            self._changed("workspace.selection.changed", selection_ids=normalized)

    def capture_panel_state(self) -> None:
        self.state.panels = {
            state.panel_id: state
            for state in self.panels.states()
        }

    def save_layout(self, name: str) -> Path:
        self.capture_panel_state()
        path = self.layouts.save(name, self.state)
        self.events.publish("workspace.layout.saved", name=name, path=str(path))
        return path

    def load_layout(self, name: str) -> WorkspaceState:
        restored = self.layouts.load(name)
        self.state = restored
        self.panels.restore(restored.panels.values())
        self.events.publish("workspace.layout.loaded", name=name)
        return restored
