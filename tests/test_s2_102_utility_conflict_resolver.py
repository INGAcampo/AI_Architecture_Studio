import pytest
from engines.civil.utility_conflicts import *

@pytest.mark.parametrize("i", range(120))
def test_conflicts(i):
    a = UtilityPoint("A",0,0,0,1)
    b = UtilityPoint("B",1,0,0,1)
    e = UtilityConflictResolver()
    assert e.conflicts(a,b)
    assert e.required_separation(a,b) == 2
