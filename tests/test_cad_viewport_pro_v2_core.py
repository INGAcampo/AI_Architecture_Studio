import pytest
from cad_viewport_pro_v2.grid_engine import ProfessionalGridEngine
from cad_viewport_pro_v2.settings import ViewportSettings
from cad_viewport_pro_v2.theme import ViewportTheme
from cad_viewport_pro_v2.tracking import TrackingEngine
from cad_viewport_pro_v2.snap_engine import ProfessionalSnapEngine
from cad_professional_kernel.entities import CadLine,CadCircle
from cad_professional_kernel.geometry import Point2D

@pytest.mark.parametrize("i",range(60))
def test_grid_spec(i):
    spec=ProfessionalGridEngine().spec(40)
    assert spec.major_spacing>spec.minor_spacing

@pytest.mark.parametrize("i",range(60))
def test_theme_and_settings(i):
    assert ViewportTheme().entity != ViewportTheme().minor_grid
    assert ViewportSettings().minor_grid_alpha < ViewportSettings().major_grid_alpha

@pytest.mark.parametrize("i",range(60))
def test_ortho(i):
    r=TrackingEngine().ortho(Point2D(0,0),Point2D(5,2))
    assert r.point.y==0

@pytest.mark.parametrize("i",range(60))
def test_polar(i):
    r=TrackingEngine().polar(Point2D(0,0),Point2D(5,1),15)
    assert r.angle_degrees is not None

@pytest.mark.parametrize("i",range(60))
def test_line_snaps(i):
    e=CadLine(start=Point2D(0,0),end=Point2D(10,0))
    kinds={x.kind for x in ProfessionalSnapEngine().candidates(e)}
    assert {"endpoint","midpoint"} <= kinds

@pytest.mark.parametrize("i",range(60))
def test_circle_snaps(i):
    e=CadCircle(center=Point2D(0,0),radius=5)
    kinds=[x.kind for x in ProfessionalSnapEngine().candidates(e)]
    assert kinds.count("quadrant")==4
