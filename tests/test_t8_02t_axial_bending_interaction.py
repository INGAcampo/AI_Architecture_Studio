import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.axial_bending_interaction import AxialBendingInteraction
    assert AxialBendingInteraction().unity(50,100,25,100)==pytest.approx(.75)
