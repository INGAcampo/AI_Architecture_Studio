import pytest
from engines.civil.rail import *
@pytest.mark.parametrize("i",range(120))
def test_rail(i):
    s=(RailSegment("A",100,0.01,500),RailSegment("B",200,-0.015,700));e=RailAlignmentEngine()
    assert e.total_length(s)==300 and e.max_gradient(s)==0.015 and e.minimum_radius(s)==500
