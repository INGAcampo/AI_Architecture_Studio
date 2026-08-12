import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.contact_domain import ContactResult
    from analysis.contact.contact_report import ContactReportEngine
    r=ContactResult((),True,3,1e-6);assert 'Advanced Nonlinear Contact Report' in ContactReportEngine().build(r,.3,'cpu').markdown
