import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.torsion_core import TorsionEngine
    assert TorsionEngine().shear_stress_mpa(1000,10,10000)==1
