import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.dynamic_vertical_slice import DynamicVerticalSlice
    r=DynamicVerticalSlice().run(((4,0),(0,9)),((1,0),(0,1)),1000,.2,.01)
    assert r.result.converged and '# Modal Seismic Dynamic' in r.report.markdown
