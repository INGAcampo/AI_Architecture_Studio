import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.matrix_analysis_vertical_slice import MatrixAnalysisVerticalSlice
    r=MatrixAnalysisVerticalSlice().run(((2,0),(0,4)),(4,8),.01)
    assert r.result.converged and '# Matrix Structural Analysis Report' in r.report.markdown
