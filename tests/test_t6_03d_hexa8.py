import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.hexa8 import Hexa8Engine
    assert sum(Hexa8Engine().shape(.1,.2,.3))==pytest.approx(1)
