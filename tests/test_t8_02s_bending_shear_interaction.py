import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.bending_shear_interaction import BendingShearInteraction
    assert BendingShearInteraction().unity(50,100,20,100)==pytest.approx(.54)
