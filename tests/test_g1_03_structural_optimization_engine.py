import pytest
from ai_kernel.structural_optimization import *

@pytest.mark.parametrize("i", range(120))
def test_structural_optimization(i):
    sections = (
        StructuralSection("S1", 0.01, 100, 20, 15),
        StructuralSection("S2", 0.02, 200, 30, 22),
        StructuralSection("S3", 0.03, 300, 45, 28),
    )
    demand = StructuralDemand(f"D{i}", 150, 6)
    engine = StructuralOptimizationEngine()
    options = engine.feasible_options(demand, sections)
    assert len(options) == 2
    best = engine.select_minimum_mass(demand, sections)
    assert best.section_id == "S2"
    assert best.utilization == pytest.approx(0.75)
