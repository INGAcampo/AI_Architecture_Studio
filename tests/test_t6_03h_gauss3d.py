import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.gauss3d import Gauss3DEngine
    assert len(Gauss3DEngine().points())==8
