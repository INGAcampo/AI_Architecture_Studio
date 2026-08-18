import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem2d.quad4_element import Quad4ElementEngine
    assert abs(sum(Quad4ElementEngine().shape(.2,-.1))-1)<1e-12
