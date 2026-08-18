import pytest
from design.steel.bolt_domain import *

@pytest.mark.parametrize("i", range(120))
def test_bolt_domain(i):
    mat=BoltMaterial(BoltGrade.A325,620e6,372e6)
    bolt=Bolt(f"B{i}",0.022,mat)
    assert bolt.diameter==pytest.approx(0.022)
    assert bolt.material.grade is BoltGrade.A325
