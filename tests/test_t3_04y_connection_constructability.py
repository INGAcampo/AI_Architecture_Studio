import pytest
from design.steel.connection_constructability import *
@pytest.mark.parametrize("i",range(120))
def test_constructability(i):
    assert 0<=ConnectionConstructabilityEngine().score(.8,.9,.2,.7).score<=1
