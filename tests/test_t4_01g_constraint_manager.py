import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.constraint_manager import ConstraintManager
    K,F=ConstraintManager().apply(((2,0),(0,3)),(1,2),(0,));assert K[0][0]==1 and F[0]==0
