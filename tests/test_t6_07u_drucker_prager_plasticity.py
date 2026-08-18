import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.drucker_prager_plasticity import DruckerPragerYieldEngine
    assert DruckerPragerYieldEngine().function(10,5,.1,3)==pytest.approx(3)
