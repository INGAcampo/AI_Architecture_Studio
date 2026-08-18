import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.fem_vertical_slice import FemVerticalSlice
    r=FemVerticalSlice().run(((2,0),(0,4)),(4,8),2,1,.8,10);assert r.result.converged and '# Finite Element' in r.report.markdown
