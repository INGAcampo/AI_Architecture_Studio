import pytest
from design.steel.weld_domain import *
from design.steel.weld_group import *
@pytest.mark.parametrize("i",range(120))
def test_group(i):
    m=WeldMaterial(ElectrodeClass.E70,490e6); s=(WeldSegment("W1",WeldType.FILLET,.008,.2,-.1,-.1,.1,-.1,m),WeldSegment("W2",WeldType.FILLET,.008,.2,-.1,.1,.1,.1,m))
    assert len(WeldGroupEngine().distribute(s,100e3,0,5e3)[1])==2
