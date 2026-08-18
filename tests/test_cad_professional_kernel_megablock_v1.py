import pytest
from pathlib import Path

from cad_professional_kernel.blocks import BlockDefinition, BlockLibrary
from cad_professional_kernel.constraints import HorizontalConstraint, VerticalConstraint
from cad_professional_kernel.diagnostics import CadDiagnostics
from cad_professional_kernel.entities import CadCircle, CadLine, CadPolyline
from cad_professional_kernel.geometry import Point2D, Vector2D
from cad_professional_kernel.layers import Layer
from cad_professional_kernel.serialization import SceneSerializer
from cad_professional_kernel.service import CadKernelService
from cad_professional_kernel.snaps import SnapEngine
from cad_professional_kernel.xrefs import ExternalReference, XrefManager

@pytest.mark.parametrize("i", range(100))
def test_geometry_and_entities(i):
    a = Point2D(0, 0)
    b = Point2D(3, 4)
    assert a.distance_to(b) == 5
    assert Vector2D(3, 4).length == 5
    assert CadLine(start=a, end=b).length == 5
    assert CadCircle(center=a, radius=2).radius == 2

@pytest.mark.parametrize("i", range(100))
def test_service_history_selection(i):
    service = CadKernelService()
    line = CadLine(start=Point2D(0,0), end=Point2D(10,0))
    entity_id = service.add(line)
    service.selection.select(entity_id)
    assert service.selection.ids() == (entity_id,)
    assert service.undo()
    assert len(service.scene.all()) == 0
    assert service.redo()
    assert len(service.scene.all()) == 1

@pytest.mark.parametrize("i", range(100))
def test_layers_blocks_snaps_constraints(i):
    service = CadKernelService()
    service.scene.layers.add(Layer("STRUCTURE"))
    service.scene.layers.set_current("STRUCTURE")
    line = CadLine(layer="STRUCTURE", start=Point2D(0,0), end=Point2D(10,0))
    service.add(line)
    snaps = SnapEngine().endpoints(line)
    assert len(snaps) == 2
    assert SnapEngine().nearest(Point2D(9,0), snaps).point == Point2D(10,0)
    assert HorizontalConstraint(Point2D(0,0), Point2D(5,8)).apply()[1] == Point2D(5,0)
    assert VerticalConstraint(Point2D(0,0), Point2D(5,8)).apply()[1] == Point2D(0,8)
    library = BlockLibrary()
    library.add(BlockDefinition("B1", [line]))
    assert len(library.instantiate("B1")) == 1

@pytest.mark.parametrize("i", range(100))
def test_serialization_diagnostics_xrefs(tmp_path, i):
    service = CadKernelService()
    service.add(CadLine(start=Point2D(0,0), end=Point2D(1,1)))
    service.add(CadCircle(center=Point2D(2,2), radius=3))
    service.add(CadPolyline(points=[Point2D(0,0), Point2D(1,0), Point2D(1,1)], closed=True))
    file = tmp_path / f"scene_{i}.json"
    SceneSerializer().save(service.scene, file)
    restored = SceneSerializer().load(file)
    assert len(restored.all()) == 3
    assert CadDiagnostics().inspect(restored)["status"] == "PASS"
    xrefs = XrefManager()
    xrefs.attach(ExternalReference("SITE", Path("site.dwg")))
    assert len(xrefs.all()) == 1
