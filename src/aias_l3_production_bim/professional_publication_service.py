"""002D project service integrating exact professional publication."""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Sequence

from .professional_documentation_service import (
    ProfessionalDocumentationProjectService,
)
from .professional_publication import ProfessionalPublicationBridge


class ProfessionalPublicationProjectService(ProfessionalDocumentationProjectService):
    """Extend 002C with layouts, title blocks, revisions and exports."""

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
        self.publication = ProfessionalPublicationBridge()

    def create_sheet_layout_item(
        self,
        *,
        item_id: str,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> Any:
        """Create exact native layout item for sheet composition."""
        return self.publication.create_layout_item(
            item_id=item_id,
            x=x,
            y=y,
            width=width,
            height=height,
        )

    def fit_sheet_layout_item(
        self,
        item_id: str,
        *,
        sheet_width: float,
        sheet_height: float,
        margin: float = 10.0,
    ) -> Any:
        """Fit one layout item using LayoutViewportManager."""
        return self.publication.fit_layout_item(
            item_id,
            sheet_width=sheet_width,
            sheet_height=sheet_height,
            margin=margin,
        )

    def arrange_sheet_layout_grid(
        self,
        item_ids: Sequence[str],
        *,
        columns: int,
        gap: float = 10.0,
    ) -> Any:
        """Arrange exact layout items into a publication grid."""
        return self.publication.arrange_layout_grid(
            item_ids,
            columns=columns,
            gap=gap,
        )

    def create_sheet_titleblock(
        self,
        *,
        titleblock_id: str,
        sheet_id: str,
    ) -> Any:
        """Create exact native title block from canonical project/sheet state."""
        sheet = self._sheet(sheet_id)
        project_name = getattr(
            getattr(self.state, "project", None),
            "name",
            None,
        ) or getattr(
            getattr(self.state, "project_info", None),
            "name",
            None,
        ) or "AIAS Project"

        return self.publication.create_titleblock(
            titleblock_id=titleblock_id,
            project_name=project_name,
            sheet_number=sheet.number,
            sheet_title=sheet.name,
        )

    def add_sheet_revision(
        self,
        titleblock_id: str,
        *,
        revision_id: str,
        description: str,
        issued_on: date,
        author: str,
    ) -> Any:
        """Append an exact native revision to a title block."""
        return self.publication.add_revision(
            titleblock_id,
            revision_id=revision_id,
            description=description,
            issued_on=issued_on,
            author=author,
        )

    def export_native_drawing(
        self,
        drawing: Any,
        output: str | Path,
    ) -> dict:
        """Export exact native drawing through DrawingExporter."""
        return self.publication.export_drawing(drawing, output)

    def export_structural_dwg(
        self,
        *,
        path: str | Path,
        sheets: Iterable[Any],
    ) -> Any:
        """Export specialized structural DWG payload."""
        return self.publication.export_structural_dwg(
            path=path,
            sheets=sheets,
        )

    def export_structural_pdf(
        self,
        *,
        path: str | Path,
        report: Any,
    ) -> Any:
        """Export specialized structural PDF payload."""
        return self.publication.export_structural_pdf(
            path=path,
            report=report,
        )

    def workspace_projection_with_publication(self) -> dict[str, Any]:
        """Extend Workspace 2 projection with publication-layer state."""
        base = self.workspace_projection_with_professional_docs()
        snap = self.publication.snapshot()

        return {
            **base,
            "professional_publication": {
                "layouts": snap.layouts,
                "titleblocks": snap.titleblocks,
                "revisions": snap.revisions,
                "exports": snap.exports,
                "layout_ids": sorted(self.publication.layout_store),
                "titleblock_ids": sorted(self.publication.titleblock_store),
            },
        }
