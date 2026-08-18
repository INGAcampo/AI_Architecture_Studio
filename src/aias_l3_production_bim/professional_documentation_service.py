"""002C project service integrating native professional documentation."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Sequence

from documentation_kernel.model import DocumentationView

from .exact_persistent_service import ExactNativePersistentProjectService
from .professional_documentation import ProfessionalDocumentationBridge


class ProfessionalDocumentationProjectService(ExactNativePersistentProjectService):
    """Extend the certified 001I workflow with professional documentation engines."""

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
            drawing_viewer=drawing_viewer,
            **kwargs,
        )
        self.professional = ProfessionalDocumentationBridge()

    def add_documentation_view(
        self,
        name: str,
        view_type: str,
        *,
        scale: float,
        level_id: str | None = None,
        **properties: Any,
    ) -> Any:
        """Register new exact native view in both 001G and 002C managers."""
        canonical = super().add_documentation_view(
            name,
            view_type,
            scale=scale,
            level_id=level_id,
            **properties,
        )
        native = self.documentation.views[canonical.id]
        self.professional.register_documentation_view(native)
        return canonical

    def generate_section_view(
        self,
        name: str,
        *,
        elements: Iterable[Any],
        cut_x: float,
        depth: float,
        scale: float,
        level_id: str | None = None,
        **properties: Any,
    ) -> Any:
        """Create canonical/native section view and generate its exact content."""
        view = self.add_documentation_view(
            name,
            "section",
            scale=scale,
            level_id=level_id,
            **properties,
        )
        self.professional.generate_section(
            view_id=view.id,
            elements=elements,
            cut_x=cut_x,
            depth=depth,
        )
        return view

    def generate_elevation_view(
        self,
        name: str,
        *,
        elements: Iterable[Any],
        direction: str,
        scale: float,
        level_id: str | None = None,
        **properties: Any,
    ) -> Any:
        """Create canonical/native elevation view and generate its exact content."""
        view = self.add_documentation_view(
            name,
            "elevation",
            scale=scale,
            level_id=level_id,
            direction=direction,
            **properties,
        )
        self.professional.generate_elevation(
            view_id=view.id,
            elements=elements,
            direction=direction,
        )
        return view

    def add_view_annotation(
        self,
        view_id: str,
        *,
        annotation_id: str,
        kind: Any,
        text: str,
        x: float,
        y: float,
        style_id: str = "default",
    ) -> Any:
        """Attach exact annotation to an activated professional view."""
        return self.professional.add_annotation(
            view_id=view_id,
            annotation_id=annotation_id,
            kind=kind,
            text=text,
            x=x,
            y=y,
            style_id=style_id,
        )

    def add_view_dimension(
        self,
        view_id: str,
        *,
        dimension_id: str,
        start: tuple[float, float],
        end: tuple[float, float],
        prefix: str = "",
        suffix: str = "",
        precision: int = 2,
    ) -> Any:
        """Create native dimension and record its view association canonically."""
        self._view(view_id)
        dimension = self.professional.add_linear_dimension(
            dimension_id=dimension_id,
            start=start,
            end=end,
            prefix=prefix,
            suffix=suffix,
            precision=precision,
        )
        view = self._view(view_id)
        items = list(view.properties.get("dimension_ids", []))
        items.append(dimension_id)
        view.properties["dimension_ids"] = items
        return dimension

    def render_element_tag(
        self,
        *,
        element_id: str,
        properties: dict[str, Any],
        template_id: str,
        pattern: str,
    ) -> Any:
        """Render one exact intelligent tag."""
        return self.professional.render_tag(
            element_id=element_id,
            properties=properties,
            template_id=template_id,
            pattern=pattern,
        )

    def build_project_schedule(
        self,
        *,
        schedule_id: str,
        elements: Iterable[Any],
        columns: Sequence[tuple[str, str]],
        predicate: Any | None = None,
        sort_key: Any | None = None,
    ) -> Any:
        """Create exact native project schedule."""
        return self.professional.build_schedule(
            schedule_id=schedule_id,
            elements=elements,
            columns=columns,
            predicate=predicate,
            sort_key=sort_key,
        )

    def workspace_projection_with_professional_docs(self) -> dict[str, Any]:
        """Extend 001I Workspace 2 projection with professional documentation state."""
        base = self.workspace_projection_with_native_docs()
        snap = self.professional.snapshot()

        return {
            **base,
            "professional_documentation": {
                "managed_views": snap.managed_views,
                "annotations": snap.annotations,
                "generated_views": snap.generated_views,
                "dimensions": snap.dimensions,
                "tags": snap.tags,
                "schedules": snap.schedules,
                "section_elevation_view_ids": sorted(
                    self.professional.generated_views
                ),
                "dimension_ids": sorted(
                    self.professional.dimension_store
                ),
                "schedule_ids": sorted(
                    self.professional.schedule_store
                ),
            },
        }
