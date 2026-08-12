import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.nonlinear_vertical_slice import NonlinearVerticalSlice
    r=NonlinearVerticalSlice().run(1000,10,.05,.04)
    assert r.result.converged and '# Nonlinear Structural Analysis Report' in r.report_markdown
