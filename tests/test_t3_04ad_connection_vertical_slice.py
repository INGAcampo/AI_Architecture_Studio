import pytest
from design.steel.connection_domain import *
from design.steel.connection_optimizer import ConnectionOption
from design.steel.connection_vertical_slice import *
@pytest.mark.parametrize("i",range(120))
def test_slice(i):
    c=SteelConnection(f"C{i}",ConnectionFamily.MOMENT,ConnectionMethod.HYBRID,"W14X38","W14X38",ConnectionDemand(moment=100e3))
    checks=(ConnectionCheck("bolt",.6,True),ConnectionCheck("weld",.5,True),ConnectionCheck("plate",.7,True))
    opts=(ConnectionOption("EP",.7,100,.8,15),ConnectionOption("DW",.6,110,.7,10))
    r=CompleteConnectionVerticalSlice().run(c,checks,opts)
    assert r.design_result.passed and "# Steel Connection Report" in r.report.markdown
