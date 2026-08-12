import pytest
from types import SimpleNamespace
from design.steel.frame_ai_advisor import SteelFrameAIAdvisor

@pytest.mark.parametrize("i", range(120))
def test_frame_ai(i):
    d=SimpleNamespace(failed_members=0,critical_members=())
    c=SimpleNamespace(valid=True)
    l=SimpleNamespace(path_exists=True)
    o=SimpleNamespace(optimized_members=1,average_weight_reduction_percent=10)
    a=SteelFrameAIAdvisor().advise(d,c,l,o)
    assert "apto" in a.summary and a.recommendations
