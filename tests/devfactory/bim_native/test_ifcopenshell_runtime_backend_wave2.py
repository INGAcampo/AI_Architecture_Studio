from __future__ import annotations

from src.engines.bim.native_ifc.runtime_backend import IfcOpenShellRuntimeBackend


def test_ifcopenshell_runtime_is_available_in_validated_wave2_environment():
    info = IfcOpenShellRuntimeBackend.discover()
    assert info.available is True
    assert info.version


def test_ifc_create_spatial_wall_roundtrip(tmp_path):
    backend = IfcOpenShellRuntimeBackend()
    model, project = backend.create_minimal_project("IFC4")
    assert project.is_a("IfcProject")

    site, building, storey = backend.add_spatial_hierarchy(model)
    wall = backend.add_wall(model, storey)

    assert site.is_a("IfcSite")
    assert building.is_a("IfcBuilding")
    assert storey.is_a("IfcBuildingStorey")
    assert wall.is_a("IfcWall")

    path = tmp_path / "wave2_runtime.ifc"
    backend.write(model, path)
    reopened = backend.open(path)

    walls = reopened.by_type("IfcWall")
    assert len(walls) == 1
    assert walls[0].GlobalId == wall.GlobalId
    assert len(reopened.by_type("IfcRelAggregates")) == 3


def test_ifcopenshell_invalid_file_fails_closed(tmp_path):
    backend = IfcOpenShellRuntimeBackend()
    path = tmp_path / "invalid.ifc"
    path.write_text("NOT AN IFC FILE", encoding="utf-8")

    failed = False
    try:
        backend.open(path)
    except Exception:
        failed = True

    assert failed is True
