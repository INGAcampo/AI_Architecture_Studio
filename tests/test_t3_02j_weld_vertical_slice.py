import pytest
from design.steel.weld_domain import *
from design.steel.weld_vertical_slice import *
@pytest.mark.parametrize("i",range(120))
def test_slice(i):
    m=WeldMaterial(ElectrodeClass.E70,490e6); s=(WeldSegment("W1",WeldType.FILLET,.008,.2,-.1,-.1,.1,-.1,m),WeldSegment("W2",WeldType.FILLET,.008,.2,-.1,.1,.1,.1,m))
    r=WeldConnectionVerticalSlice().run(s,100e3,20e3,5e3,10e3)
    assert len(r.design_results)==2 and "# Weld Connection" in r.report.markdown
