import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.tension_block_shear import BlockShearEngine
    assert BlockShearEngine().nominal_strength_n(1000,800,300,250,400)>0
