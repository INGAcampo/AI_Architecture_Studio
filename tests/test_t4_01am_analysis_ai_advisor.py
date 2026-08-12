import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from types import SimpleNamespace
    from analysis.matrix.analysis_ai_advisor import AnalysisAIAdvisor
    assert 'estable' in AnalysisAIAdvisor().advise(SimpleNamespace(converged=True),SimpleNamespace(warnings=()),.01).summary
