import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.vonmises3d import VonMises3DEngine
    assert VonMises3DEngine().calculate(10,0,0)==pytest.approx(10)
