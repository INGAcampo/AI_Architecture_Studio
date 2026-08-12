import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.mohr_coulomb_plasticity import MohrCoulombYieldEngine
    assert isinstance(MohrCoulombYieldEngine().function(10,2,30,1),float)
