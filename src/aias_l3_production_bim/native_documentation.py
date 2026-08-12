"""Exact native documentation bridge for AIAS L3 Production BIM 001G."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from documentation_kernel.model import DocumentationView, Sheet, Viewport
from documentation_kernel.sheets import SheetManager


class NativeDocumentationContractError(RuntimeError):
    """Raised when native documentation invariants cannot be satisfied."""


@dataclass(slots=True)
class NativeDocumentationSnapshot:
    """Expose native documentation counts without leaking manager internals."""

    views: int
    sheets: int
    viewports: int


class NativeDocumentationBridge:
    """Manage exact DocumentationView / Sheet / Viewport native entities."""

    def __init__(self, drawing_viewer: Any | None = None) -> None:
        self.sheet_manager = SheetManager()
        self.drawing_viewer = drawing_viewer
        self.views: dict[str, DocumentationView] = {}

    def create_view(
        self,
        *,
        view_id: str,
        name: str,
        scale: float,
        model_revision: int = 0,
        metadata: dict[str, Any] | None = None,
    ) -> DocumentationView:
        """Create and register an exact native documentation view."""
        if view_id in self.views:
            raise NativeDocumentationContractError(f"duplicate_native_view:{view_id}")

        view = DocumentationView(
            view_id=view_id,
            name=name,
            scale=float(scale),
            model_revision=int(model_revision),
            metadata=dict(metadata or {}),
        )
        self.views[view_id] = view
        return view

    def create_sheet(
        self,
        *,
        sheet_id: str,
        number: str,
        title: str,
        width: float,
        height: float,
    ) -> Sheet:
        """Create and register an exact native drawing sheet."""
        sheet = Sheet(
            sheet_id=sheet_id,
            number=number,
            title=title,
            width=float(width),
            height=float(height),
        )
        self.sheet_manager.add(sheet)
        return sheet

    def place_viewport(
        self,
        *,
        sheet_id: str,
        viewport_id: str,
        view_id: str,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> Sheet:
        """Place a native viewport through the audited SheetManager contract."""
        if view_id not in self.views:
            raise NativeDocumentationContractError(f"unknown_native_view:{view_id}")

        viewport = Viewport(
            viewport_id=viewport_id,
            view_id=view_id,
            x=float(x),
            y=float(y),
            width=float(width),
            height=float(height),
        )
        return self.sheet_manager.place_viewport(sheet_id, viewport)

    def show_sheet(self, sheet_id: str, drawing_viewer: Any | None = None) -> Any:
        """Display a native sheet through DrawingViewer.show_sheet(sheet)."""
        viewer = drawing_viewer if drawing_viewer is not None else self.drawing_viewer
        if viewer is None:
            raise NativeDocumentationContractError("drawing_viewer_required")
        show = getattr(viewer, "show_sheet", None)
        if not callable(show):
            raise NativeDocumentationContractError("drawing_viewer_missing_show_sheet")
        return show(self.sheet_manager.get(sheet_id))

    def snapshot(self) -> NativeDocumentationSnapshot:
        """Return native documentation inventory."""
        sheets = self.sheet_manager.all()
        return NativeDocumentationSnapshot(
            views=len(self.views),
            sheets=len(sheets),
            viewports=sum(len(sheet.viewports) for sheet in sheets),
        )
