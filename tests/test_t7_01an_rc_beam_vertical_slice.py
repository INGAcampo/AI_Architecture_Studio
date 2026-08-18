import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.rc_beam_vertical_slice import RCBeamVerticalSlice
    r=RCBeamVerticalSlice().run();assert r.result.status=='PASS' and '# Reinforced Concrete Beam Design' in r.report.markdown
