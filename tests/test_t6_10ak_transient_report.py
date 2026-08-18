import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.transient_domain import TransientResult
    from analysis.transient.transient_report import TransientReportEngine
    assert 'Transient Dynamics Report' in TransientReportEngine().build(TransientResult((),True,'X'),1,2,.01,'cpu').markdown
