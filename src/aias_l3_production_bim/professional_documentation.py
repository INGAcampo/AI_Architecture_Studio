"""Professional documentation activation for AIAS L3 Production BIM 002C."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from documentation_kernel.section_elevation import SectionElevationGenerator
from documentation_kernel.smart_dimensions import SmartDimensionEngine, Dimension, DimensionPoint
from documentation_kernel.views import ViewManager
from documentation_kernel.model import Annotation, AnnotationKind, DocumentationView
from documentation_kernel.intelligent_tags import IntelligentTagEngine, TagTemplate
from documentation_kernel.schedule_engine import ScheduleEngine, ScheduleColumn, Schedule


class ProfessionalDocumentationError(RuntimeError):
    """Raised when an exact professional-documentation contract cannot be satisfied."""


@dataclass(slots=True)
class ProfessionalDocumentationSnapshot:
    """Concise inventory of activated professional-documentation state."""

    managed_views: int
    annotations: int
    generated_views: int
    dimensions: int
    tags: int
    schedules: int


class ProfessionalDocumentationBridge:
    """Activate exact native documentation-kernel authorities audited by 002B."""

    def __init__(self) -> None:
        self.section_elevation = SectionElevationGenerator()
        self.dimensions = SmartDimensionEngine()
        self.views = ViewManager()
        self.tags = IntelligentTagEngine()
        self.schedules = ScheduleEngine()

        self.generated_views: dict[str, Any] = {}
        self.dimension_store: dict[str, Dimension] = {}
        self.tag_store: dict[str, Any] = {}
        self.schedule_store: dict[str, Schedule] = {}

    def register_documentation_view(
        self,
        view: DocumentationView,
        *,
        replace_existing: bool = False,
    ) -> DocumentationView:
        """Register an exact native DocumentationView with ViewManager."""
        self.views.add(view, replace_existing=replace_existing)
        return view

    def generate_section(
        self,
        *,
        view_id: str,
        elements: Iterable[Any],
        cut_x: float,
        depth: float,
    ) -> Any:
        """Generate a native section from model elements."""
        result = self.section_elevation.section(
            view_id,
            list(elements),
            float(cut_x),
            float(depth),
        )
        self.generated_views[view_id] = result
        return result

    def generate_elevation(
        self,
        *,
        view_id: str,
        elements: Iterable[Any],
        direction: str = "north",
    ) -> Any:
        """Generate a native elevation from model elements."""
        result = self.section_elevation.elevation(
            view_id,
            list(elements),
            direction=direction,
        )
        self.generated_views[view_id] = result
        return result

    def add_linear_dimension(
        self,
        *,
        dimension_id: str,
        start: tuple[float, float],
        end: tuple[float, float],
        prefix: str = "",
        suffix: str = "",
        precision: int = 2,
    ) -> Dimension:
        """Create an exact native linear dimension."""
        start_point = (
            start
            if isinstance(start, DimensionPoint)
            else DimensionPoint(float(start[0]), float(start[1]))
        )
        end_point = (
            end
            if isinstance(end, DimensionPoint)
            else DimensionPoint(float(end[0]), float(end[1]))
        )
        dimension = self.dimensions.linear(
            dimension_id,
            start_point,
            end_point,
            prefix=prefix,
            suffix=suffix,
            precision=int(precision),
        )
        self.dimension_store[dimension_id] = dimension
        return dimension

    def dimension_chain_total(self, dimension_ids: Sequence[str]) -> float:
        """Return the exact native total for a dimension chain."""
        dimensions = [self.dimension_store[item] for item in dimension_ids]
        return self.dimensions.chain_total(dimensions)

    def duplicate_dimensions(
        self,
        dimension_ids: Sequence[str],
        *,
        tolerance: float = 1e-9,
    ) -> Any:
        """Detect duplicate dimensions through SmartDimensionEngine."""
        dimensions = [self.dimension_store[item] for item in dimension_ids]
        return self.dimensions.detect_duplicates(
            dimensions,
            tolerance=float(tolerance),
        )

    def add_annotation(
        self,
        *,
        view_id: str,
        annotation_id: str,
        kind: AnnotationKind | str,
        text: str,
        x: float,
        y: float,
        style_id: str = "default",
    ) -> Annotation:
        """Attach an exact native Annotation to a managed DocumentationView."""
        if isinstance(kind, str):
            try:
                kind = AnnotationKind(kind)
            except ValueError as exc:
                raise ProfessionalDocumentationError(
                    f"unknown_annotation_kind:{kind}"
                ) from exc

        annotation = Annotation(
            annotation_id=annotation_id,
            kind=kind,
            text=text,
            x=float(x),
            y=float(y),
            style_id=style_id,
        )
        self.views.add_annotation(view_id, annotation)
        return annotation

    def update_view_revision(self, view_id: str, revision: int) -> Any:
        """Update native documentation-view revision through ViewManager."""
        return self.views.update_revision(view_id, int(revision))

    def render_tag(
        self,
        *,
        element_id: str,
        properties: dict[str, Any],
        template_id: str,
        pattern: str,
    ) -> Any:
        """Render one intelligent tag using the exact native tag engine."""
        template = TagTemplate(template_id, pattern)
        result = self.tags.render(element_id, dict(properties), template)
        self.tag_store[element_id] = result
        return result

    def batch_render_tags(
        self,
        *,
        elements: Iterable[Any],
        template_id: str,
        pattern: str,
    ) -> Any:
        """Render intelligent tags in batch using the native engine."""
        template = TagTemplate(template_id, pattern)
        result = self.tags.batch_render(list(elements), template)
        for index, item in enumerate(result):
            self.tag_store[f"{template_id}:{index}"] = item
        return result

    def build_schedule(
        self,
        *,
        schedule_id: str,
        elements: Iterable[Any],
        columns: Sequence[tuple[str, str]],
        predicate: Any | None = None,
        sort_key: Any | None = None,
    ) -> Schedule:
        """Build an exact native schedule."""
        native_columns = tuple(
            ScheduleColumn(key=key, heading=heading)
            for key, heading in columns
        )
        schedule = self.schedules.build(
            schedule_id,
            list(elements),
            native_columns,
            predicate=predicate,
            sort_key=sort_key,
        )
        self.schedule_store[schedule_id] = schedule
        return schedule

    def schedule_total(self, schedule_id: str, column_index: int) -> Any:
        """Aggregate one native schedule column."""
        return self.schedules.total(
            self.schedule_store[schedule_id],
            int(column_index),
        )

    def snapshot(self) -> ProfessionalDocumentationSnapshot:
        """Return current professional-documentation inventory."""
        managed_views = self.views.all()
        annotation_count = sum(
            len(getattr(view, "annotations", ()) or ())
            for view in managed_views
        )
        return ProfessionalDocumentationSnapshot(
            managed_views=len(managed_views),
            annotations=annotation_count,
            generated_views=len(self.generated_views),
            dimensions=len(self.dimension_store),
            tags=len(self.tag_store),
            schedules=len(self.schedule_store),
        )
