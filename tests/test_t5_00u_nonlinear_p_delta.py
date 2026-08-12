import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.nonlinear_p_delta import Engine
    assert Engine().calculate(1,2,3)==6
