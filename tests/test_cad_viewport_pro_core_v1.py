import pytest
from cad_viewport_pro.camera import Camera2D
from cad_viewport_pro.grid import AdaptiveGrid
from cad_viewport_pro.math2d import ViewTransform
from cad_viewport_pro.hit_test import HitTester
from cad_professional_kernel.entities import CadLine,CadCircle
from cad_professional_kernel.geometry import Point2D

@pytest.mark.parametrize("i",range(50))
def test_camera(i):
    c=Camera2D(); c.pan(2,3); c.zoom_by(2)
    assert (c.center_x,c.center_y,c.zoom)==(2,3,2)

@pytest.mark.parametrize("i",range(50))
def test_transform(i):
    t=ViewTransform(1000,800,0,0,10); s=t.world_to_screen(5,-2); w=t.screen_to_world(s.x,s.y)
    assert w.x==pytest.approx(5) and w.y==pytest.approx(-2)

@pytest.mark.parametrize("i",range(50))
def test_grid(i):
    assert AdaptiveGrid().spacing(10)>0

@pytest.mark.parametrize("i",range(50))
def test_hit_line(i):
    assert HitTester().hit(CadLine(start=Point2D(0,0),end=Point2D(10,0)),Point2D(5,.1),.2)

@pytest.mark.parametrize("i",range(50))
def test_hit_circle(i):
    assert HitTester().hit(CadCircle(center=Point2D(0,0),radius=5),Point2D(5,.1),.2)
