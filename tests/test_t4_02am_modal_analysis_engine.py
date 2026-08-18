import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.modal_analysis_engine import ModalAnalysisEngine
    assert len(ModalAnalysisEngine().solve(((4,0),(0,9)),((1,0),(0,1))).modes)==2
