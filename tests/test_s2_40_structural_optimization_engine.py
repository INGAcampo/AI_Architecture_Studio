import pytest
from engines.structural.optimization import *

@pytest.mark.parametrize("index", range(120))
def test_optimization(index):
    engine = StructuralOptimizationEngine()
    candidates = (
        DesignCandidate(f"A{index}", 100 + index, 0.8, 0.01),
        DesignCandidate(f"B{index}", 120 + index, 0.7, 0.005),
    )
    selected = engine.select_lightest(candidates, max_ratio=1.0, max_displacement=0.02)
    assert selected.candidate_id == f"A{index}"
