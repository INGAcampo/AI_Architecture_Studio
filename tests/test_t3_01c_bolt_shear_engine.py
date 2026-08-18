import pytest
from design.steel.bolt_domain import *
from design.steel.bolt_shear import BoltShearEngine

@pytest.mark.parametrize("i", range(120))
def test_bolt_shear(i):
    b=Bolt(f"B{i}",0.022,BoltMaterial(BoltGrade.A325,620e6,372e6))
    r=BoltShearEngine().calculate(b,2)
    assert r.design_capacity>0
    assert r.planes==2
