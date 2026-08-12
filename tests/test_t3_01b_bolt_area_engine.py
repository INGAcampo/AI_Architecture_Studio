import pytest
from design.steel.bolt_domain import *
from design.steel.bolt_area import BoltAreaEngine

@pytest.mark.parametrize("i", range(120))
def test_bolt_area(i):
    b=Bolt(f"B{i}",0.02,BoltMaterial(BoltGrade.A325,620e6,372e6))
    r=BoltAreaEngine().calculate(b)
    assert r.gross_area>r.tensile_area
    assert r.shear_area==pytest.approx(r.tensile_area)
