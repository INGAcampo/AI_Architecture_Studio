"""Focused regression for L3-PRODUCTION-BIM-002D."""
from datetime import date
from pathlib import Path

from aias_l3_production_bim.professional_publication_service import (
    ProfessionalPublicationProjectService,
)


def _discovery() -> Path:
    return Path("AIAS_L3_PRODUCTION_BIM_DISCOVERY_CURRENT") / "DISCOVERY.json"


def _service():
    service = ProfessionalPublicationProjectService(
        "002D Test",
        discovery_path=_discovery(),
    )
    service.start()
    return service


def test_002d_layout_item_fit_and_grid():
    service = _service()

    service.create_sheet_layout_item(
        item_id="VP-A",
        x=0.0,
        y=0.0,
        width=300.0,
        height=200.0,
    )
    service.create_sheet_layout_item(
        item_id="VP-B",
        x=0.0,
        y=0.0,
        width=250.0,
        height=180.0,
    )

    fitted = service.fit_sheet_layout_item(
        "VP-A",
        sheet_width=841.0,
        sheet_height=594.0,
        margin=20.0,
    )
    arranged = service.arrange_sheet_layout_grid(
        ("VP-A", "VP-B"),
        columns=2,
        gap=15.0,
    )

    assert fitted is not None
    assert arranged is not None


def test_002d_titleblock_and_revision():
    service = _service()
    sheet = service.add_documentation_sheet(
        "A101",
        "Ground Floor Plan",
        width=841.0,
        height=594.0,
    )

    titleblock = service.create_sheet_titleblock(
        titleblock_id="TB-A101",
        sheet_id=sheet.id,
    )
    revision = service.add_sheet_revision(
        "TB-A101",
        revision_id="R1",
        description="Issued for coordination",
        issued_on=date(2026, 8, 7),
        author="AIAS",
    )

    latest = service.publication.latest_revision("TB-A101")
    stored = service.publication.titleblock_store["TB-A101"]

    assert titleblock.titleblock_id == "TB-A101"
    assert revision.revision_id == "R1"
    assert stored.titleblock_id == "TB-A101"
    assert latest is not None
    assert latest.revision_id == "R1"


def test_002d_workspace_projection_contains_publication_state():
    service = _service()
    service.create_sheet_layout_item(
        item_id="VP-A",
        x=10.0,
        y=20.0,
        width=300.0,
        height=200.0,
    )

    sheet = service.add_documentation_sheet(
        "A201",
        "Sections",
        width=841.0,
        height=594.0,
    )
    service.create_sheet_titleblock(
        titleblock_id="TB-A201",
        sheet_id=sheet.id,
    )

    projection = service.workspace_projection_with_publication()

    pub = projection["professional_publication"]
    assert pub["layouts"] == 1
    assert pub["titleblocks"] == 1
    assert "VP-A" in pub["layout_ids"]
    assert "TB-A201" in pub["titleblock_ids"]
