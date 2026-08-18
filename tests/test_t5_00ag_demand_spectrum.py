import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.demand_spectrum import DemandSpectrumEngine
    assert DemandSpectrumEngine().spectral_displacement(1,1)>0
