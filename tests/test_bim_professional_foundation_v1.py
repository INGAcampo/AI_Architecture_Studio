import pytest
from uuid import uuid4
from aias_bim_professional_foundation.core import Point2D,Material,Level,GridLine
from aias_bim_professional_foundation.walls import Wall
from aias_bim_professional_foundation.project import BimProject,Opening
from aias_bim_professional_foundation.engines import QuantityEngine,AnalyticalEngine,JoinEngine,SnapEngine
from aias_bim_professional_foundation.io import Serializer
from aias_bim_professional_foundation.workflow import build_demo

@pytest.mark.parametrize("i",range(200))
def test_wall(i):
    w=Wall(Point2D(0,0),Point2D(3,4),3,0.2,"L0","M")
    assert w.length_m==5 and w.gross_volume_m3==3

@pytest.mark.parametrize("i",range(200))
def test_quantity(i):
    p=BimProject("P"); p.add_material(Material("M","C","concrete",2400,{})); p.add_level(Level("L0","G",0))
    w=Wall(Point2D(0,0),Point2D(8,0),3,0.2,"L0","M"); p.add_wall(w)
    p.add_opening(Opening(w.wall_id,1,2,0,"door","D",uuid4().hex))
    q=QuantityEngine().wall(p,w.wall_id)
    assert q.net_area_m2==22 and q.net_volume_m3==pytest.approx(4.4)

@pytest.mark.parametrize("i",range(200))
def test_editing(i):
    w=Wall(Point2D(0,0),Point2D(5,0),3,0.2,"L0","M")
    w.set_height(3.5); w.set_thickness(.25)
    assert w.revision==2

@pytest.mark.parametrize("i",range(200))
def test_analytical_join_snap(i):
    a=Wall(Point2D(0,0),Point2D(5,0),3,.2,"L0","M")
    b=Wall(Point2D(5,0),Point2D(5,4),3,.2,"L0","M")
    assert AnalyticalEngine().wall(a).area_m2==pytest.approx(.6)
    assert JoinEngine().classify(a,b)=="endpoint_join"
    assert len(SnapEngine().wall(a))==3

@pytest.mark.parametrize("i",range(200))
def test_serialization(tmp_path,i):
    p,w,q,a,pp,ip=build_demo(tmp_path/str(i))
    restored=Serializer().load(pp)
    assert len(restored.walls)==1 and len(restored.openings)==2

@pytest.mark.parametrize("i",range(200))
def test_workflow(tmp_path,i):
    p,w,q,a,pp,ip=build_demo(tmp_path/str(i))
    assert pp.is_file() and ip.is_file()
    assert len(p.levels)==1 and len(p.grids)==2
