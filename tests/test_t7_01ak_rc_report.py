import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.rc_domain import RCBeamInput,RCBeamResult
    from analysis.rc.rc_report import RCReportEngine
    b=RCBeamInput('B',1,1,1,1,1,1,1);r=RCBeamResult(1,1,1,1,.5,'PASS');assert 'Reinforced Concrete Beam Design' in RCReportEngine().build(b,r).markdown
