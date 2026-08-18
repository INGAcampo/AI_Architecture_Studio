import pytest
from design.steel.brace_report_advisor import *
from types import SimpleNamespace

@pytest.mark.parametrize("i", range(120))
def test_report_advisor(i):
    batch=SimpleNamespace(results=(SimpleNamespace(member_id="BR1",unity_ratio=0.95,passed=True,governing_check="compression"),),passed_count=1,failed_count=0,maximum_unity=0.95)
    a=BraceReportAdvisor()
    assert "BR1" in a.build_report(batch).markdown
    assert a.advise(batch).critical_members==("BR1",)
