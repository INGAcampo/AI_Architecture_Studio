import pytest
from design.steel.bolt_domain import *
from design.steel.bolt_design_engine import BoltDesignEngine

@pytest.mark.parametrize("i", range(120))
def test_bolt_design(i):
    bolt=Bolt(f"B{i}",0.022,BoltMaterial(BoltGrade.A325,620e6,372e6))
    demand=BoltGroupDemand(shear_x=50e3,tension=20e3)
    r=BoltDesignEngine().design(bolt,demand,0.012,450e6,0.04,0.07)
    assert r.unity_ratio>=0
    assert r.shear_capacity>0
