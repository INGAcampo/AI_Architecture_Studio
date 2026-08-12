import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_stability.stability_vertical_slice import StabilityVerticalSlice
    r=StabilityVerticalSlice().run()
    assert r[2].status=='PASS' and 'Steel Stability Report' in r[-1]
