import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.dynamic_domain import DynamicAnalysisResult
    from analysis.dynamic.dynamic_report import DynamicReportEngine
    r=DynamicAnalysisResult((),(),(),True)
    assert 'Modal Seismic Dynamic' in DynamicReportEngine().build(r,100,.01).markdown
