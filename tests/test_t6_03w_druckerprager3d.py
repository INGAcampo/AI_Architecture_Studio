import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.druckerprager3d import Engine
    assert Engine().calculate(1,2,3)==6
