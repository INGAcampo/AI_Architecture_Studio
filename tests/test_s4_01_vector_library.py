import pytest
from engines.numerical.vectors import *

@pytest.mark.parametrize("i", range(120))
def test_vectors(i):
    a=DenseVector((1,2,3)); b=DenseVector((4,5,6))
    assert a.add(b).values==(5.0,7.0,9.0)
    assert b.subtract(a).values==(3.0,3.0,3.0)
    assert a.dot(b)==pytest.approx(32)
    assert a.scale(2).norm()==pytest.approx((4+16+36)**0.5)
