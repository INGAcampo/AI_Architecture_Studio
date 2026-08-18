import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.contact_vertical_slice import ContactVerticalSlice
    r=ContactVerticalSlice().run();assert r.result.converged and '# Advanced Nonlinear Contact Report' in r.report.markdown
