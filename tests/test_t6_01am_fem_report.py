import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.fem_domain import FemAnalysisResult
    from analysis.fem.fem_report import FemReportEngine
    assert 'Finite Element' in FemReportEngine().build(FemAnalysisResult((1,),(0,),True),2,1,10).markdown
