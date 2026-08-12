import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.beam_deflection import BeamDeflectionEngine
    assert BeamDeflectionEngine().simply_supported_uniform_mm(1,1000,200000,1e8)>0
