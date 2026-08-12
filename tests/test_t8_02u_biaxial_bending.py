import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.biaxial_bending import BiaxialBendingEngine
    assert BiaxialBendingEngine().unity(40,100,20,100)==pytest.approx(.6)
