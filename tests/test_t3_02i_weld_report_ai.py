import pytest
from types import SimpleNamespace
from design.steel.weld_report_ai import *
@pytest.mark.parametrize("i",range(120))
def test_report(i):
    r=SimpleNamespace(segment_id="W1",unity_ratio=.5,governing_check="shear",passed=True)
    assert "W1" in WeldReportAI().build((r,)).markdown
