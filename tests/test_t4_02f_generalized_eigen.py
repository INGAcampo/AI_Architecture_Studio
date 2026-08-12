import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.generalized_eigen import GeneralizedEigenEngine
    assert GeneralizedEigenEngine().solve(((4,0),(0,9)),((1,0),(0,1)))[0]==(4.0,9.0)
