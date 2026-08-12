import pytest
from types import SimpleNamespace
from design.steel.frame_batch_design import FrameBatchDesignEngine

@pytest.mark.parametrize("i", range(120))
def test_batch_design(i):
    a=SimpleNamespace(member_id="B1",unity_ratio=0.5,passed=True,governing_check="flexure")
    b=SimpleNamespace(member_id="C1",unity_ratio=0.8,passed=True,governing_check="interaction")
    r=FrameBatchDesignEngine().design((a,),(b,),())
    assert r.passed_count==2 and r.maximum_unity==pytest.approx(0.8)
