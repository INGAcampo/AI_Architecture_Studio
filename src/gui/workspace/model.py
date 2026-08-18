from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import uuid4
from aias_i18n import tr


class DockArea(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    FLOATING = "floating"
    CENTER = "center"


@dataclass(frozen=True, slots=True)
class PanelDescriptor:
    panel_id: str
    title: str
    default_area: DockArea = DockArea.RIGHT
    singleton: bool = True
    category: str = "general"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.panel_id.strip():
            raise ValueError("panel_id no puede estar vacío")
        if not self.title.strip():
            raise ValueError("title no puede estar vacío")


@dataclass(slots=True)
class PanelState:
    panel_id: str
    area: DockArea
    visible: bool = True
    floating: bool = False
    auto_hide: bool = False
    order: int = 0
    geometry: tuple[int, int, int, int] | None = None

    def snapshot(self) -> dict[str, Any]:
        return {
            "panel_id": self.panel_id,
            "area": self.area.value,
            "visible": self.visible,
            "floating": self.floating,
            "auto_hide": self.auto_hide,
            "order": self.order,
            "geometry": list(self.geometry) if self.geometry else None,
        }

    @classmethod
    def from_snapshot(cls, data: dict[str, Any]) -> "PanelState":
        geometry = data.get("geometry")
        return cls(
            panel_id=str(data["panel_id"]),
            area=DockArea(data["area"]),
            visible=bool(data.get("visible", True)),
            floating=bool(data.get("floating", False)),
            auto_hide=bool(data.get("auto_hide", False)),
            order=int(data.get("order", 0)),
            geometry=tuple(geometry) if geometry is not None else None,
        )


@dataclass(slots=True)
class DocumentSession:
    path: str | None = None
    title: str = field(default_factory=lambda: tr("document.untitled"))
    document_id: str = field(default_factory=lambda: str(uuid4()))
    modified: bool = False
    active_view_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.path and self.title == tr("document.untitled"):
            self.title = Path(self.path).stem

    def mark_modified(self, value: bool = True) -> None:
        self.modified = bool(value)

    def snapshot(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "path": self.path,
            "title": self.title,
            "modified": self.modified,
            "active_view_id": self.active_view_id,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_snapshot(cls, data: dict[str, Any]) -> "DocumentSession":
        return cls(
            document_id=str(data["document_id"]),
            path=data.get("path"),
            title=str(data.get("title", tr("document.untitled"))),
            modified=bool(data.get("modified", False)),
            active_view_id=data.get("active_view_id"),
            metadata=dict(data.get("metadata", {})),
        )


@dataclass(slots=True)
class WorkspaceState:
    name: str = "default"
    active_document_id: str | None = None
    active_tool: str | None = None
    selection_ids: tuple[str, ...] = ()
    panels: dict[str, PanelState] = field(default_factory=dict)
    documents: dict[str, DocumentSession] = field(default_factory=dict)
    revision: int = 0

    def touch(self) -> int:
        self.revision += 1
        return self.revision

    def snapshot(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "name": self.name,
            "active_document_id": self.active_document_id,
            "active_tool": self.active_tool,
            "selection_ids": list(self.selection_ids),
            "panels": {
                key: value.snapshot()
                for key, value in sorted(self.panels.items())
            },
            "documents": {
                key: value.snapshot()
                for key, value in sorted(self.documents.items())
            },
            "revision": self.revision,
        }

    @classmethod
    def from_snapshot(cls, data: dict[str, Any]) -> "WorkspaceState":
        if int(data.get("schema_version", 1)) != 1:
            raise ValueError("Versión de WorkspaceState no soportada")
        return cls(
            name=str(data.get("name", "default")),
            active_document_id=data.get("active_document_id"),
            active_tool=data.get("active_tool"),
            selection_ids=tuple(str(item) for item in data.get("selection_ids", [])),
            panels={
                key: PanelState.from_snapshot(value)
                for key, value in data.get("panels", {}).items()
            },
            documents={
                key: DocumentSession.from_snapshot(value)
                for key, value in data.get("documents", {}).items()
            },
            revision=int(data.get("revision", 0)),
        )
