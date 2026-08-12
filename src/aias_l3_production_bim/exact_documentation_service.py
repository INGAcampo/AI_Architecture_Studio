"""001G exact native project authoring: Level/Grid + Views/Sheets/Viewports."""
from __future__ import annotations

from pathlib import Path
from typing import Any
import uuid

from .exact_native_service import ExactNativeProjectAuthoringService
from .native_documentation import NativeDocumentationBridge


def _viewport_id() -> str:
    return f"VP-{uuid.uuid4().hex[:12].upper()}"


class ExactNativeDocumentationProjectService(ExactNativeProjectAuthoringService):
    """Add explicit native documentation authoring to the 001F project workflow."""

    def __init__(
        self,
        project_name: str,
        *,
        discovery_path: Path,
        drawing_viewer: Any | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            project_name,
            discovery_path=discovery_path,
            **kwargs,
        )
        self.documentation = NativeDocumentationBridge(drawing_viewer=drawing_viewer)

    def add_documentation_view(
        self,
        name: str,
        view_type: str,
        *,
        scale: float,
        level_id: str | None = None,
        **properties: Any,
    ) -> Any:
        """Create canonical ProjectView plus exact native DocumentationView."""
        before = self.state.clone()
        history_len = len(self._history)
        redo = list(self._redo)

        try:
            canonical = self.add_view(
                name,
                view_type,
                level_id=level_id,
                scale=float(scale),
                **properties,
            )
            self.documentation.create_view(
                view_id=canonical.id,
                name=canonical.name,
                scale=float(scale),
                model_revision=self.state.revision,
                metadata={
                    "view_type": canonical.view_type,
                    "level_id": canonical.level_id,
                    **dict(canonical.properties),
                },
            )
            return canonical
        except Exception:
            self.state = before
            del self._history[history_len:]
            self._redo = redo
            raise

    def add_documentation_plan_view(
        self,
        name: str,
        level_id: str,
        *,
        scale: float,
        **properties: Any,
    ) -> Any:
        """Create a plan view with an explicit professional drawing scale."""
        return self.add_documentation_view(
            name,
            "plan",
            scale=scale,
            level_id=level_id,
            **properties,
        )

    def add_documentation_sheet(
        self,
        number: str,
        name: str,
        *,
        width: float,
        height: float,
    ) -> Any:
        """Create canonical Sheet plus exact native documentation Sheet."""
        before = self.state.clone()
        history_len = len(self._history)
        redo = list(self._redo)

        try:
            canonical = self.add_sheet(number, name)
            canonical.properties["width"] = float(width)
            canonical.properties["height"] = float(height)
            self.documentation.create_sheet(
                sheet_id=canonical.id,
                number=canonical.number,
                title=canonical.name,
                width=float(width),
                height=float(height),
            )
            return canonical
        except Exception:
            self.state = before
            del self._history[history_len:]
            self._redo = redo
            raise

    def place_documentation_view_on_sheet(
        self,
        sheet_id: str,
        view_id: str,
        *,
        x: float,
        y: float,
        width: float,
        height: float,
        viewport_id: str | None = None,
    ) -> str:
        """Place canonical view and exact native Viewport transactionally."""
        before = self.state.clone()
        history_len = len(self._history)
        redo = list(self._redo)
        vp_id = viewport_id or _viewport_id()

        try:
            # Validate canonical references before native mutation.
            self._sheet(sheet_id)
            self._view(view_id)

            self.documentation.place_viewport(
                sheet_id=sheet_id,
                viewport_id=vp_id,
                view_id=view_id,
                x=x,
                y=y,
                width=width,
                height=height,
            )
            self.place_view_on_sheet(sheet_id, view_id)
            return vp_id
        except Exception:
            self.state = before
            del self._history[history_len:]
            self._redo = redo
            raise

    def show_documentation_sheet(
        self,
        sheet_id: str,
        *,
        drawing_viewer: Any | None = None,
    ) -> Any:
        """Render/show the exact native sheet through DrawingViewer.show_sheet."""
        self._sheet(sheet_id)
        return self.documentation.show_sheet(
            sheet_id,
            drawing_viewer=drawing_viewer,
        )

    def professional_documentation_snapshot(self) -> dict[str, Any]:
        """Return combined canonical/native documentation state."""
        native = self.documentation.snapshot()
        return {
            "canonical_views": len(self.state.views),
            "canonical_sheets": len(self.state.sheets),
            "native_views": native.views,
            "native_sheets": native.sheets,
            "native_viewports": native.viewports,
        }

    def exact_native_report(self) -> dict[str, Any]:
        """Extend 001F report with exact views/sheets/viewports integration."""
        report = super().exact_native_report()
        report["exact_native_domains"] = [
            "levels",
            "grids",
            "views",
            "documentation",
        ]
        report["documentation"] = self.professional_documentation_snapshot()
        return report
