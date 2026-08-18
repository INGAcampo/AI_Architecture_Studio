import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.tension_gross_yield import TensionGrossYieldEngine
    assert TensionGrossYieldEngine().nominal_strength_n(1000,250)==250000
