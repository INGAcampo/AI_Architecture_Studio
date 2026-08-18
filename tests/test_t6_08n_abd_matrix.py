import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.abd_matrix import ABDMatrixEngine
    A,B,D=ABDMatrixEngine().build_isotropic(10,.3,.2);assert A[0][0]>D[0][0]>0
