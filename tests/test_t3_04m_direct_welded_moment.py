import pytest
from design.steel.direct_welded_moment import *
@pytest.mark.parametrize("i",range(120))
def test_direct(i):
    assert DirectWeldedMomentEngine().design(100e3,.5,300e3,50e3,100e3).passed
