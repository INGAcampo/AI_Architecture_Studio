import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.finite_rotation import FiniteRotationEngine
    matrix=FiniteRotationEngine().matrix_2d(0)
    assert matrix[0] == pytest.approx((1,0))
    assert matrix[1] == pytest.approx((0,1))
