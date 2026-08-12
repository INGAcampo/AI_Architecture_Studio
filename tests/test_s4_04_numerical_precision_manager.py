import pytest
from engines.numerical.precision import *

@pytest.mark.parametrize("i", range(120))
def test_precision(i):
    p=NumericalPrecisionManager(PrecisionPolicy(1e-10,1e-8,100))
    assert p.close(1.0,1.0+1e-9)
    assert p.vector_close((1,2),(1+1e-9,2-1e-9))
    assert p.is_zero(1e-12)
