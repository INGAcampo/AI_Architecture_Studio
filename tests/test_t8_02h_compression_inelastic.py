import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.compression_inelastic import InelasticCompressionEngine
    assert InelasticCompressionEngine().critical_stress_mpa(345,200000,80)>0
