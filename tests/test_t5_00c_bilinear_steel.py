import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.bilinear_steel import BilinearSteelModel
    assert BilinearSteelModel().stress(.001,200e9,250e6)>0
