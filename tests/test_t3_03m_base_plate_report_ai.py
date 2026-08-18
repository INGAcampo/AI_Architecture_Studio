import pytest
from types import SimpleNamespace
from design.steel.base_plate_report_ai import *
@pytest.mark.parametrize("i",range(120))
def test_report(i):
    p=SimpleNamespace(plate_id="P",width=.5,length=.5,thickness=.03)
    r=SimpleNamespace(maximum_unity=.5,governing_check="plate",passed=True)
    assert "Base Plate" in BasePlateReportAI().build(p,r).markdown
