import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.lap_splice import Engine
    assert Engine().calculate(1,2,3)==6
