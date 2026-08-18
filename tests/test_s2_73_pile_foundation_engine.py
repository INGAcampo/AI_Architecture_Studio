import pytest
from engines.geotechnical.piles import *
@pytest.mark.parametrize("i",range(120))
def test_pile(i):
    p=Pile(f"P{i}",.4+i*.001,10,1500,60); e=PileFoundationEngine()
    assert e.ultimate_capacity(p)>e.allowable_capacity(p)
