import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.transient_vertical_slice import TransientVerticalSlice
    r=TransientVerticalSlice().run();assert r.result.converged and '# Implicit & Explicit Transient Dynamics Report' in r.report.markdown
