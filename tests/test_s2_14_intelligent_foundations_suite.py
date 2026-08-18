import pytest
from engines.structural.foundations import *

@pytest.mark.parametrize("kind", list(FoundationKind))
def test_kinds(kind): assert kind.value

@pytest.mark.parametrize("length,width,depth", [(1,1,.4),(1.5,1.5,.5),(2,2,.6),(2.5,2,.7),(3,3,.8),(4,2,1),(5,1,.5),(6,2,.8),(8,4,1.2),(10,5,1.5)])
def test_geometry(length,width,depth):
    f=IntelligentFoundation("f",FoundationKind.ISOLATED,"m",length,width,depth)
    assert f.volume == pytest.approx(length*width*depth)

@pytest.mark.parametrize("density", [1800,2000,2200,2300,2400,2500,2600,2700,2800,3000])
def test_material_density(density): assert FoundationMaterial("m","M",density).density==density

@pytest.mark.parametrize("index", range(10))
def test_catalog(index):
    c=FoundationMaterialCatalog(); m=FoundationMaterial(f"m{index}",f"M{index}",2400)
    c.register(m); assert c.get(m.material_id) is m; assert c.remove(m.material_id) is m

def make_engine():
    e=IntelligentFoundationEngine(); e.register_material(FoundationMaterial("c","Concrete",2400)); return e

@pytest.mark.parametrize("index", range(20))
def test_add_foundations(index):
    e=make_engine(); f=IntelligentFoundation(f"f{index}",FoundationKind.ISOLATED,"c",1+index*.1,1,0.5)
    e.add_foundation(f); assert e.get(f.foundation_id) is f

@pytest.mark.parametrize("load", [100e3,200e3,300e3,400e3,500e3,600e3,700e3,800e3,900e3,1e6])
def test_contact_pressure(load):
    e=make_engine(); e.add_foundation(IntelligentFoundation("f",FoundationKind.ISOLATED,"c",2,2,.5))
    assert e.calculate("f",load).contact_pressure == pytest.approx(load/4)

@pytest.mark.parametrize("index", range(10))
def test_resize(index):
    e=make_engine(); e.add_foundation(IntelligentFoundation("f",FoundationKind.ISOLATED,"c",1,1,.5))
    e.resize("f",2+index,3,.6); assert e.get("f").length == 2+index

def test_validation():
    with pytest.raises(ValueError): IntelligentFoundation("",FoundationKind.ISOLATED,"m",1,1,1)
    with pytest.raises(ValueError): FoundationMaterial("","M",2400)
def test_quantities():
    e=make_engine(); e.add_foundation(IntelligentFoundation("f",FoundationKind.ISOLATED,"c",2,2,.5))
    q=e.calculate("f"); assert q.concrete_volume==2; assert q.mass==4800
def test_parameters():
    ids={d.parameter_id for d in foundation_parameter_definitions()}; assert {"length","width","depth","plan_area","volume"}<=ids
def test_events():
    events=[]; e=IntelligentFoundationEngine(lambda n,p:events.append((n,p)))
    e.register_material(FoundationMaterial("c","Concrete",2400)); e.add_foundation(IntelligentFoundation("f",FoundationKind.ISOLATED,"c",1,1,.5))
    assert events[-1][0]=="foundation.added"

@pytest.mark.parametrize("index", range(39))
def test_additional_foundation_cases(index):
    f=IntelligentFoundation(f"x{index}",FoundationKind.PEDESTAL,"m",1+index*.01,1,.5)
    assert f.plan_area > 0
