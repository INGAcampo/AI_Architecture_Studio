import pytest
from engines.bim.facades import *

@pytest.mark.parametrize("kind",list(FacadePanelKind))
def test_panel_kinds(kind):assert kind.value
@pytest.mark.parametrize("u,v",[(1,1),(2,1),(2,2),(3,2),(4,3),(5,4),(6,5),(8,6),(10,8),(12,10)])
def test_grid(u,v):assert FacadeGrid(u,v).panel_count==u*v
@pytest.mark.parametrize("transparency",[0,.1,.2,.3,.4,.5,.6,.7,.8,1])
def test_transparency(transparency):assert FacadePanelType("p","P",FacadePanelKind.GLASS,.02,transparency=transparency).transparency==transparency
@pytest.mark.parametrize("width,height",[(1,1),(2,1),(2,2),(3,2),(4,3),(5,4),(6,5),(8,6),(10,8),(12,10)])
def test_area(width,height):
    f=IntelligentCurtainWall("f",width,height,FacadeGrid(2,2),"p");assert f.gross_area==width*height
@pytest.mark.parametrize("index",range(10))
def test_catalog(index):
    c=FacadePanelCatalog();p=FacadePanelType(f"p{index}",f"P{index}",FacadePanelKind.GLASS,.02)
    c.register(p);assert c.get(p.type_id) is p;assert c.remove(p.type_id) is p

def make_engine():
    e=IntelligentFacadeEngine()
    e.register_panel_type(FacadePanelType("glass","Glass",FacadePanelKind.GLASS,.02))
    e.register_panel_type(FacadePanelType("opaque","Opaque",FacadePanelKind.OPAQUE,.08))
    return e

@pytest.mark.parametrize("index",range(20))
def test_add_facades(index):
    e=make_engine();f=IntelligentCurtainWall(f"f{index}",6,3,FacadeGrid(3,2),"glass")
    e.add(f);assert e.get(f.facade_id) is f

@pytest.mark.parametrize("index",range(10))
def test_overrides(index):
    e=make_engine();f=IntelligentCurtainWall("f",10,5,FacadeGrid(5,2),"glass");e.add(f)
    u=index%5;v=index//5;e.override_panel("f",u,v,"opaque");assert e.get("f").panel_overrides[(u,v)]=="opaque"

def test_validation():
    with pytest.raises(ValueError):FacadeGrid(0,1)
    with pytest.raises(ValueError):FacadePanelType("","P",FacadePanelKind.GLASS,.02)
def test_quantities():
    e=make_engine();e.add(IntelligentCurtainWall("f",10,5,FacadeGrid(5,2),"glass"))
    q=e.calculate("f");assert q.panel_count==10;assert q.glass_area==50
def test_override_quantities():
    e=make_engine();e.add(IntelligentCurtainWall("f",10,5,FacadeGrid(5,2),"glass"));e.override_panel("f",0,0,"opaque")
    q=e.calculate("f");assert q.opaque_area==5;assert q.glass_area==45
def test_parameters():
    ids={d.parameter_id for d in facade_parameter_definitions()};assert {"width","height","gross_area","glass_area","panel_count"}<=ids
def test_events():
    events=[];e=IntelligentFacadeEngine(lambda n,p:events.append((n,p)))
    e.register_panel_type(FacadePanelType("glass","Glass",FacadePanelKind.GLASS,.02));e.add(IntelligentCurtainWall("f",2,2,FacadeGrid(2,2),"glass"))
    assert events[-1][0]=="facade.added"

@pytest.mark.parametrize("index",range(40))
def test_additional_facade_cases(index):
    f=IntelligentCurtainWall(f"x{index}",4+index*.1,3,FacadeGrid(2,2),"p")
    assert f.panel_width>0
