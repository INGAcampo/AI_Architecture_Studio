import pytest
from types import SimpleNamespace
from design.steel.critical_dashboard import CriticalMemberDashboardEngine

@pytest.mark.parametrize("i", range(120))
def test_dashboard(i):
    rec=SimpleNamespace(member_id="C1",member_type="column",unity_ratio=0.95,governing_check="interaction")
    batch=SimpleNamespace(records=(rec,),passed_count=1,failed_count=0,maximum_unity=0.95)
    d=CriticalMemberDashboardEngine().build(batch)
    assert d.critical_members[0].member_id=="C1"
