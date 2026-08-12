import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.tetra4 import Tetra4Engine
    assert Tetra4Engine().volume(((0,0,0),(1,0,0),(0,1,0),(0,0,1)))==pytest.approx(1/6)
