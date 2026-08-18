import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.elasticity3d import Elasticity3DEngine
    assert Elasticity3DEngine().matrix(200e9,.3)[0][0]>0
