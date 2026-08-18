import pytest
from ai_kernel.energy_optimization import *

@pytest.mark.parametrize("i", range(120))
def test_energy(i):
    variants = (
        EnergyVariant("A", 180, 0.30, 3.0, 0.8),
        EnergyVariant("B", 90, 0.25, 4.0, 0.6),
    )
    engine = EnergyOptimizationEngine()
    score = engine.evaluate(variants[0])
    assert score.total_energy > 0
    assert score.daylight > 0
    assert engine.select_minimum_energy(variants).variant_id in {"A", "B"}
