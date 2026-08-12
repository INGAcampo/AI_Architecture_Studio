import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.mass_matrix import MassMatrixEngine
    assert MassMatrixEngine().lumped((2,3))[1][1]==3
