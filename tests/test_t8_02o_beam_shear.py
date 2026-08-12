import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.beam_shear import BeamShearEngine
    assert BeamShearEngine().nominal_strength_n(250,1000)==150000
