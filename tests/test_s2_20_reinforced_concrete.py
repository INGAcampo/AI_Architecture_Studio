import pytest
from engines.structural.reinforced_concrete import *
@pytest.mark.parametrize("kind",list(RcMemberKind))
def test_kinds(kind):assert kind.value
@pytest.mark.parametrize("d",[.006,.008,.01,.012,.014,.016,.018,.02,.025,.032])
def test_rebar_area(d):assert Rebar("R",d,1,1).area_each>0
@pytest.mark.parametrize("count",range(1,21))
def test_total_area(count):assert Rebar("R",.016,count,1).total_area==pytest.approx(Rebar("X",.016,1,1).area_each*count)
@pytest.mark.parametrize("index",range(30))
def test_steel_mass(index):
    m=RcMember(f"M{index}",RcMemberKind.BEAM,1,(Rebar("R",.016,4,index+1),));assert ReinforcedConcreteEngine().steel_mass(m)>0
def test_validation():
    with pytest.raises(ValueError):Rebar("",.016,1,1)
@pytest.mark.parametrize("index",range(54))
def test_ratio(index):
    m=RcMember(f"M{index}",RcMemberKind.COLUMN,1+index*.1,(Rebar("R",.02,8,3),));assert ReinforcedConcreteEngine().ratio(m)>0
