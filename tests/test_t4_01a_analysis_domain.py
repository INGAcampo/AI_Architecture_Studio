import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.analysis_domain import AnalysisResult
    assert AnalysisResult((1,),(0,),True).converged
