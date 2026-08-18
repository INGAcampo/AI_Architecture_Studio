import pytest
from design.steel.brace_domain import *

@pytest.mark.parametrize("i", range(120))
def test_brace_domain(i):
    b=SteelBrace(
        f"BR{i}","HSS200X200X8","ASTM_A992",4.0,1.0,
        BraceBehavior.TENSION_COMPRESSION,BraceConfiguration.X_BRACE,
        SteelBraceDemand(250e3)
    )
    assert b.length==pytest.approx(4.0)
    assert b.configuration is BraceConfiguration.X_BRACE
