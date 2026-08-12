import pytest
from design.steel.bolt_domain import *
from design.steel.bolt_tension import BoltTensionEngine

@pytest.mark.parametrize("i", range(120))
def test_bolt_tension(i):
    b=Bolt(f"B{i}",0.022,BoltMaterial(BoltGrade.A490,780e6,468e6))
    r=BoltTensionEngine().calculate(b)
    assert r.design_capacity>0
