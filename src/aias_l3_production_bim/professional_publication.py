"""Professional publication layer for AIAS L3 Production BIM 002D."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Sequence

from documentation_kernel.layout_viewports import LayoutItem, LayoutViewportManager
from documentation_kernel.titleblock_revision import (
    Revision,
    TitleBlock,
    TitleBlockRevisionManager,
)
from aias_drawing_framework.exporters import DrawingExporter
from engines.structural.dwg_exporter import DwgExporter
from engines.structural.pdf_report_exporter import PdfReportExporter


class ProfessionalPublicationError(RuntimeError):
    """Raised when an exact native publication contract cannot be satisfied."""


@dataclass(slots=True)
class PublicationSnapshot:
    """Current publication-layer inventory."""

    layouts: int
    titleblocks: int
    revisions: int
    exports: int


class ProfessionalPublicationBridge:
    """Activate exact layout, title block, revision and export authorities."""

    def __init__(self) -> None:
        self.layouts = LayoutViewportManager()
        self.titleblocks = TitleBlockRevisionManager()
        self.drawing_exporter = DrawingExporter()

        self.layout_store: dict[str, LayoutItem] = {}
        self.titleblock_store: dict[str, TitleBlock] = {}
        self.export_log: list[dict[str, Any]] = []

    def create_layout_item(
        self,
        *,
        item_id: str,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> LayoutItem:
        """Create and retain one exact native layout item."""
        item = LayoutItem(
            item_id=item_id,
            x=float(x),
            y=float(y),
            width=float(width),
            height=float(height),
        )
        self.layout_store[item_id] = item
        return item

    def fit_layout_item(
        self,
        item_id: str,
        *,
        sheet_width: float,
        sheet_height: float,
        margin: float = 10.0,
    ) -> Any:
        """Fit one exact native layout item to a sheet."""
        return self.layouts.fit(
            self.layout_store[item_id],
            float(sheet_width),
            float(sheet_height),
            margin=float(margin),
        )

    def arrange_layout_grid(
        self,
        item_ids: Sequence[str],
        *,
        columns: int,
        gap: float = 10.0,
    ) -> Any:
        """Arrange exact native layout items in a grid."""
        items = [self.layout_store[item_id] for item_id in item_ids]
        return self.layouts.arrange_grid(
            items,
            int(columns),
            gap=float(gap),
        )

    def create_titleblock(
        self,
        *,
        titleblock_id: str,
        project_name: str,
        sheet_number: str,
        sheet_title: str,
    ) -> TitleBlock:
        """Create one exact native title block."""
        titleblock = TitleBlock(
            titleblock_id=titleblock_id,
            project_name=project_name,
            sheet_number=sheet_number,
            sheet_title=sheet_title,
        )
        self.titleblock_store[titleblock_id] = titleblock
        return titleblock

    def add_revision(
        self,
        titleblock_id: str,
        *,
        revision_id: str,
        description: str,
        issued_on: date,
        author: str,
    ) -> Revision:
        """Append an exact native revision to a title block."""
        titleblock = self.titleblock_store[titleblock_id]
        revision = Revision(
            revision_id=revision_id,
            description=description,
            issued_on=issued_on,
            author=author,
        )
        updated = self.titleblocks.add_revision(titleblock, revision)
        if isinstance(updated, TitleBlock):
            self.titleblock_store[titleblock_id] = updated
        else:
            # The native manager may mutate in place and return None.
            self.titleblock_store[titleblock_id] = titleblock
        return revision

    def latest_revision(self, titleblock_id: str) -> Revision | None:
        """Return latest exact native title-block revision."""
        return self.titleblocks.latest_revision(
            self.titleblock_store[titleblock_id]
        )

    def export_drawing(self, drawing: Any, output: str | Path) -> dict:
        """Export a native drawing through the generic DrawingExporter."""
        path = Path(output)
        result = self.drawing_exporter.export(drawing, path)
        self.export_log.append({
            "kind": "drawing",
            "output": str(path),
            "result": result,
        })
        return result

    def export_structural_dwg(
        self,
        *,
        path: str | Path,
        sheets: Iterable[Any],
    ) -> Any:
        """Invoke the specialized structural DWG exporter by exact audited contract."""
        result = DwgExporter.export(str(path), list(sheets))
        self.export_log.append({
            "kind": "dwg",
            "output": str(path),
            "result": result,
        })
        return result

    def export_structural_pdf(
        self,
        *,
        path: str | Path,
        report: Any,
    ) -> Any:
        """Invoke the specialized structural PDF exporter by exact audited contract."""
        result = PdfReportExporter.export(str(path), report)
        self.export_log.append({
            "kind": "pdf",
            "output": str(path),
            "result": result,
        })
        return result

    def snapshot(self) -> PublicationSnapshot:
        """Return current publication inventory."""
        revision_count = sum(
            len(getattr(titleblock, "revisions", ()) or ())
            for titleblock in self.titleblock_store.values()
        )
        return PublicationSnapshot(
            layouts=len(self.layout_store),
            titleblocks=len(self.titleblock_store),
            revisions=revision_count,
            exports=len(self.export_log),
        )
