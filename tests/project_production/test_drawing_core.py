from aias_building_design_core import BuildingDesignCore
from aias_drawing_core import DrawingCore


def test_generates_required_views_and_pdf(tmp_path):
    graph = BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot Building"))
    model = DrawingCore().build(graph, {"status": "PASS"})
    assert DrawingCore().validate(model) == []
    assert {"Architectural Plan", "Structural Plan", "Foundation Plan", "Building Section", "Building Elevation"} <= {s["title"] for s in model.sheets}
    digest = DrawingCore().export_pdf(model, tmp_path / "PILOT-BUILDING-001.pdf")
    assert len(digest) == 64 and (tmp_path / "PILOT-BUILDING-001.pdf").read_bytes().startswith(b"%PDF")
