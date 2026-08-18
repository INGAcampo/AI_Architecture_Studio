"""Persistence, rehydration and Workspace 2 coordination for 001I."""
from __future__ import annotations

from pathlib import Path
from typing import Any
import inspect

from .exact_documentation_service import ExactNativeDocumentationProjectService
from .native_documentation import NativeDocumentationBridge


class ExactNativePersistenceError(RuntimeError):
    """Raised when Level 3 exact-native persistence cannot be completed safely."""


def _invoke_path_method(bound_method: Any, path: str | Path) -> Any:
    """Invoke an audited persistence method using its actual runtime signature."""
    sig = inspect.signature(bound_method)
    params = [
        p
        for p in sig.parameters.values()
        if p.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    ]
    required = [p for p in params if p.default is inspect.Parameter.empty]

    # Bound methods no longer expose self. AIAS persistence contracts audited in
    # 001H are accepted only when they require zero or one user argument.
    if len(required) == 0:
        if not params:
            return bound_method()
        # Prefer an explicit path-like parameter when optional.
        for p in params:
            if p.name.lower() in {
                "path",
                "file",
                "filepath",
                "file_path",
                "project_path",
                "filename",
            }:
                return bound_method(**{p.name: str(path)})
        return bound_method()

    if len(required) == 1:
        p = required[0]
        if p.kind is inspect.Parameter.KEYWORD_ONLY:
            return bound_method(**{p.name: str(path)})
        return bound_method(str(path))

    raise ExactNativePersistenceError(
        f"unsupported_persistence_signature:{bound_method.__name__}{sig}"
    )


class ExactNativePersistentProjectService(ExactNativeDocumentationProjectService):
    """Persist exact documentation layout and rebuild it after canonical reopen."""

    VIEWPORT_LAYOUT_KEY = "native_viewports"

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
        """Persist exact viewport geometry into canonical Sheet properties."""
        vp_id = super().place_documentation_view_on_sheet(
            sheet_id,
            view_id,
            x=x,
            y=y,
            width=width,
            height=height,
            viewport_id=viewport_id,
        )

        sheet = self._sheet(sheet_id)
        layout = list(sheet.properties.get(self.VIEWPORT_LAYOUT_KEY, []))
        layout.append(
            {
                "viewport_id": vp_id,
                "view_id": view_id,
                "x": float(x),
                "y": float(y),
                "width": float(width),
                "height": float(height),
            }
        )
        sheet.properties[self.VIEWPORT_LAYOUT_KEY] = layout
        return vp_id

    def rebuild_exact_native_state(self) -> dict[str, Any]:
        """Rehydrate Level/Grid and documentation native mirrors from canonical state."""
        # Replace transient native bridges with clean instances.
        from .native_level_grid import NativeLevelGridBridge

        self.level_grid = NativeLevelGridBridge()
        self.documentation = NativeDocumentationBridge(
            drawing_viewer=self.documentation.drawing_viewer
        )

        # Rehydrate exact Level/Grid mirrors.
        for level in self.state.levels.values():
            self.level_grid.mirror_level(level)

        for grid in self.state.grids.values():
            self.level_grid.mirror_grid(grid)

        # Rehydrate exact DocumentationView objects only for views with explicit scale.
        for view in self.state.views.values():
            scale = view.properties.get("scale")
            if scale is None:
                continue
            self.documentation.create_view(
                view_id=view.id,
                name=view.name,
                scale=float(scale),
                model_revision=self.state.revision,
                metadata={
                    "view_type": view.view_type,
                    "level_id": view.level_id,
                    **dict(view.properties),
                },
            )

        # Rehydrate sheets, then exact viewport geometry.
        for sheet in self.state.sheets.values():
            if "width" not in sheet.properties or "height" not in sheet.properties:
                continue

            self.documentation.create_sheet(
                sheet_id=sheet.id,
                number=sheet.number,
                title=sheet.name,
                width=float(sheet.properties["width"]),
                height=float(sheet.properties["height"]),
            )

            for item in sheet.properties.get(self.VIEWPORT_LAYOUT_KEY, []):
                self.documentation.place_viewport(
                    sheet_id=sheet.id,
                    viewport_id=item["viewport_id"],
                    view_id=item["view_id"],
                    x=float(item["x"]),
                    y=float(item["y"]),
                    width=float(item["width"]),
                    height=float(item["height"]),
                )

        return self.exact_native_report()

    def save_exact(self, path: str | Path) -> Any:
        """Persist canonical state after validating exact viewport layout is embedded."""
        for sheet in self.state.sheets.values():
            for item in sheet.properties.get(self.VIEWPORT_LAYOUT_KEY, []):
                required = {
                    "viewport_id",
                    "view_id",
                    "x",
                    "y",
                    "width",
                    "height",
                }
                if not required.issubset(item):
                    raise ExactNativePersistenceError(
                        f"incomplete_viewport_layout:{sheet.id}"
                    )
        return _invoke_path_method(self.save, path)

    def reopen_exact(self, path: str | Path) -> "ExactNativePersistentProjectService":
        """Reopen canonical project and rebuild all exact native mirrors."""
        result = _invoke_path_method(self.reopen, path)

        target = result if isinstance(result, ExactNativePersistentProjectService) else self
        if result is not None and result is not self and hasattr(result, "state"):
            # Some reopen contracts return a base service instance. Preserve the
            # reopened canonical state on this exact-native service.
            self.state = result.state
            if hasattr(result, "_history"):
                self._history = result._history
            if hasattr(result, "_redo"):
                self._redo = result._redo
            target = self

        target.rebuild_exact_native_state()
        return target

    def workspace_projection_with_native_docs(self) -> dict[str, Any]:
        """Extend audited Workspace 2 projection with exact documentation state."""
        base = self.workspace_projection()
        if not isinstance(base, dict):
            base = {"canonical_projection": base}

        native_docs = []
        for native_sheet in self.documentation.sheet_manager.all():
            native_docs.append(
                {
                    "sheet_id": native_sheet.sheet_id,
                    "number": native_sheet.number,
                    "title": native_sheet.title,
                    "width": native_sheet.width,
                    "height": native_sheet.height,
                    "viewports": [
                        {
                            "viewport_id": vp.viewport_id,
                            "view_id": vp.view_id,
                            "x": vp.x,
                            "y": vp.y,
                            "width": vp.width,
                            "height": vp.height,
                        }
                        for vp in native_sheet.viewports
                    ],
                }
            )

        return {
            **base,
            "exact_native_documentation": {
                "views": sorted(self.documentation.views),
                "sheets": native_docs,
            },
            "exact_native_domains": [
                "levels",
                "grids",
                "views",
                "documentation",
                "persistence",
                "workspace2",
            ],
        }
