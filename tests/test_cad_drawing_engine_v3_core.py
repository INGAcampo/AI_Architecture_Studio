import pytest
from cad_drawing_engine_v3.commands import LineCommand,CircleCommand,PolylineCommand
from cad_drawing_engine_v3.controller import DrawingController
from cad_drawing_engine_v3.grips import GripEngine
from cad_drawing_engine_v3.transform_ops import TransformEngine
from cad_professional_kernel.entities import CadLine,CadCircle,CadPolyline
from cad_professional_kernel.geometry import Point2D
from cad_professional_kernel.service import CadKernelService

@pytest.mark.parametrize("i",range(100))
def test_line_command(i):
    c=LineCommand(); c.click(Point2D(0,0)); r=c.click(Point2D(3,4))
    assert r.length==5 and c.finished

@pytest.mark.parametrize("i",range(100))
def test_circle_command(i):
    c=CircleCommand(); c.click(Point2D(0,0)); r=c.click(Point2D(0,5))
    assert r.radius==5

@pytest.mark.parametrize("i",range(100))
def test_polyline_command(i):
    c=PolylineCommand(); c.click(Point2D(0,0)); c.click(Point2D(1,0)); r=c.finish(True)
    assert r.closed and len(r.points)==2

@pytest.mark.parametrize("i",range(100))
def test_grips(i):
    e=CadLine(start=Point2D(0,0),end=Point2D(10,0))
    assert len(GripEngine().grips(e))==3

@pytest.mark.parametrize("i",range(100))
def test_transforms(i):
    e=CadCircle(center=Point2D(1,1),radius=2)
    m=TransformEngine().move(e,2,3)
    s=TransformEngine().scale(e,Point2D(0,0),2)
    assert m.center==Point2D(3,4) and s.radius==4

@pytest.mark.parametrize("i",range(100))
def test_controller(i):
    k=CadKernelService(); c=DrawingController(k); c.start("LINE")
    c.click(Point2D(0,0)); c.move(Point2D(2,0)); c.click(Point2D(2,0))
    assert len(k.scene.all())==1 and c.active is None
