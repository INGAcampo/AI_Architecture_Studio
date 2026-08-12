import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.analysis_domain import AnalysisResult
    from analysis.matrix.analysis_report import AnalysisReportEngine
    assert 'Matrix Structural Analysis' in AnalysisReportEngine().build(AnalysisResult((1,),(0,),True),.01).markdown
