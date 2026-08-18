import pytest
from engines.civil.parametric_intersections import *

@pytest.mark.parametrize("i", range(120))
def test_network(i):
    j = Junction(f"J{i}", ("A","B","C"), 15)
    e = ParametricIntersectionNetwork()
    assert e.degree(j) == 3
    assert e.is_valid(j)
