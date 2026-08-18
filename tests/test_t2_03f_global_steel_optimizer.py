import pytest
from types import SimpleNamespace
from design.steel.global_optimizer import GlobalSteelOptimizer

@pytest.mark.parametrize("i", range(120))
def test_global_optimizer(i):
    r1=SimpleNamespace(member_id="B1",current_profile_id="W14X38",recommended_profile_id="W12X26",weight_reduction_percent=31.63)
    r2=SimpleNamespace(member_id="C1",current_profile_id="W14X38",recommended_profile_id="W14X38",weight_reduction_percent=0.0)
    r=GlobalSteelOptimizer().combine(r1,r2)
    assert r.optimized_members==1
    assert r.average_weight_reduction_percent==pytest.approx(15.815)
