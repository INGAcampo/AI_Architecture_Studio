import pytest
from types import SimpleNamespace
from design.steel.connection_domain import *
from design.steel.connection_report import *
@pytest.mark.parametrize("i",range(120))
def test_report(i):
    c=SteelConnection("C",ConnectionFamily.SHEAR,ConnectionMethod.BOLTED,"B","C",ConnectionDemand())
    r=SimpleNamespace(unity_ratio=.5,governing_check="shear",passed=True)
    a=SimpleNamespace(summary="OK")
    assert "Steel Connection Report" in ConnectionReportEngine().build(c,r,a).markdown
