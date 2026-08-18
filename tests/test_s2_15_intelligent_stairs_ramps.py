import pytest
from engines.bim.circulation import *

@pytest.mark.parametrize("kind",list(CirculationKind))
def test_kinds(kind): assert kind.value

@pytest.mark.parametrize("rise", [2.4,2.7,3.0,3.15,3.3,3.6,4.0,4.5,5.0,6.0])
def test_risers(rise):
    item=IntelligentCirculation("s",CirculationKind.STRAIGHT_STAIR,0,rise,1.2)
    assert item.riser_count>0

@pytest.mark.parametrize("width",[.8,.9,1,1.1,1.2,1.5,1.8,2,2.5,3])
def test_width(width):
    item=IntelligentCirculation("s",CirculationKind.STRAIGHT_STAIR,0,3,width)
    assert item.width==width

@pytest.mark.parametrize("tread",[.22,.23,.24,.25,.26,.27,.28,.29,.30,.32])
def test_treads(tread):
    item=IntelligentCirculation("s",CirculationKind.STRAIGHT_STAIR,0,3,1.2,tread_depth=tread)
    assert item.tread_depth==tread

@pytest.mark.parametrize("run",[5,6,7,8,9,10,12,15,20,25])
def test_ramp_slope(run):
    item=IntelligentCirculation("r",CirculationKind.RAMP,0,.6,1.2,run_length=run)
    assert item.slope==pytest.approx(.6/run)

def make_engine(): return IntelligentCirculationEngine()

@pytest.mark.parametrize("index",range(20))
def test_add_stairs(index):
    e=make_engine(); item=IntelligentCirculation(f"s{index}",CirculationKind.U_STAIR,0,3,1.2,landing_count=1)
    e.add(item); assert e.get(item.circulation_id) is item

@pytest.mark.parametrize("index",range(10))
def test_quantities(index):
    e=make_engine(); item=IntelligentCirculation(f"s{index}",CirculationKind.STRAIGHT_STAIR,0,3,1.2)
    e.add(item); q=e.calculate(item.circulation_id); assert q.rise==3; assert q.path_length>3

def test_validation():
    with pytest.raises(ValueError): IntelligentCirculation("",CirculationKind.STRAIGHT_STAIR,0,3,1)
def test_invalid_ramp():
    e=make_engine()
    with pytest.raises(ValueError): e.add(IntelligentCirculation("r",CirculationKind.RAMP,0,1,1,run_length=5))
def test_parameters():
    ids={d.parameter_id for d in circulation_parameter_definitions()}; assert {"rise","width","riser_height","tread_depth","path_length"}<=ids
def test_events():
    events=[]; e=IntelligentCirculationEngine(lambda n,p:events.append((n,p)))
    e.add(IntelligentCirculation("s",CirculationKind.STRAIGHT_STAIR,0,3,1.2)); assert events[-1][0]=="circulation.added"

@pytest.mark.parametrize("index",range(41))
def test_additional_circulation_cases(index):
    item=IntelligentCirculation(f"x{index}",CirculationKind.STRAIGHT_STAIR,0,3,1.0+index*.01)
    assert item.path_length>0
