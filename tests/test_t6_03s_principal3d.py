import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.principal3d import Principal3DEngine
    assert Principal3DEngine().diagonal(1,3,2)==(3,2,1)
