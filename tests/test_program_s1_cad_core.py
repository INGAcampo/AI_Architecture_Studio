import pytest
from pathlib import Path
from aias_program_s1_cad.annotations import LinearDimension
from aias_program_s1_cad.blocks import BlockEngine
from aias_program_s1_cad.command_engine import CommandEngine
from aias_program_s1_cad.document import DocumentSerializer
from aias_program_s1_cad.editing import EditingEngine
from aias_program_s1_cad.entities import Line,Circle,Arc,Polyline,Ellipse,Polygon
from aias_program_s1_cad.geometry import Point,BoundingBox
from aias_program_s1_cad.layers import LayerEngine
from aias_program_s1_cad.selection import SelectionEngine
from aias_program_s1_cad.service import CadFoundationService
from aias_program_s1_cad.snaps import SnapEngine

@pytest.mark.parametrize("i",range(100))
def test_geometry_entities(i):
    assert Line(start=Point(0,0),end=Point(3,4)).length==5
    assert Circle(center=Point(0,0),radius=2).area>12
    assert Ellipse(center=Point(0,0),radius_x=2,radius_y=1).area>6
    assert Polyline(points=[Point(0,0),Point(3,4)]).length==5

@pytest.mark.parametrize("i",range(100))
def test_editing(i):
    engine=EditingEngine()
    line=Line(start=Point(0,0),end=Point(1,0))
    moved=engine.move(line,2,3)
    rotated=engine.rotate(line,Point(0,0),90)
    scaled=engine.scale(line,Point(0,0),2)
    assert moved.start==Point(2,3)
    assert rotated.end.x==pytest.approx(0,abs=1e-8)
    assert scaled.end==Point(2,0)

@pytest.mark.parametrize("i",range(100))
def test_selection(i):
    entities=[Line(start=Point(0,0),end=Point(1,1)),Circle(center=Point(10,10),radius=1)]
    engine=SelectionEngine()
    assert len(engine.window(entities,BoundingBox(-1,-1,2,2)))==1
    assert len(engine.crossing(entities,BoundingBox(.5,.5,11,11)))==2

@pytest.mark.parametrize("i",range(100))
def test_snaps_layers_blocks(i):
    line=Line(start=Point(0,0),end=Point(10,0))
    assert len(SnapEngine().candidates(line))==3
    layers=LayerEngine(); layers.create("A"); layers.set_current("A")
    assert layers.current=="A"
    blocks=BlockEngine(); blocks.create("B",[line],{"TAG":"X"})
    assert len(blocks.insert("B"))==1

@pytest.mark.parametrize("i",range(100))
def test_document_roundtrip(tmp_path,i):
    entities=[
        Line(start=Point(0,0),end=Point(1,1)),
        Circle(center=Point(2,2),radius=3),
        Arc(center=Point(0,0),radius=2,start_angle=0,end_angle=180),
        Polyline(points=[Point(0,0),Point(1,2)],closed=False),
        Ellipse(center=Point(5,5),radius_x=2,radius_y=1),
        Polygon(points=[Point(0,0),Point(1,0),Point(0,1)]),
    ]
    path=tmp_path/f"doc_{i}.json"
    DocumentSerializer().save(entities,path)
    restored=DocumentSerializer().load(path)
    assert len(restored)==6

@pytest.mark.parametrize("i",range(100))
def test_command_engine(i):
    engine=CommandEngine()
    engine.register("ADD",lambda a,b:int(a)+int(b),aliases=("A",))
    assert engine.execute("A 2 3")==5
    assert engine.history[-1]=="A 2 3"

@pytest.mark.parametrize("i",range(100))
def test_service_and_annotations(i):
    service=CadFoundationService()
    entity=Line(start=Point(0,0),end=Point(4,0))
    service.add(entity)
    assert len(service.entities)==1
    assert LinearDimension(Point(0,0),Point(4,0)).measured_value==4
