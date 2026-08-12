import pytest
from design.steel.bolt_group import *

@pytest.mark.parametrize("i", range(120))
def test_bolt_group(i):
    pts=(BoltPoint("B1",-0.05,-0.05),BoltPoint("B2",0.05,-0.05),BoltPoint("B3",0.05,0.05),BoltPoint("B4",-0.05,0.05))
    r=BoltGroupEngine().distribute(pts,100e3,0,10e3)
    assert len(r)==4
    assert max(x.resultant for x in r)>0
