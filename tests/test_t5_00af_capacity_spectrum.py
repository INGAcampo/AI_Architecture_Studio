import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.capacity_spectrum import CapacitySpectrumEngine
    assert CapacitySpectrumEngine().convert(100,1000,.1)==(.1,.1)
