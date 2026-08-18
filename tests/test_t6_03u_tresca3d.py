import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.tresca3d import Tresca3DEngine
    assert Tresca3DEngine().calculate((10,3,-2))==12
