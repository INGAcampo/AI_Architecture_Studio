import pytest
from engines.structural.water import *

@pytest.mark.parametrize("index", range(120))
def test_water(index):
    use = WaterUse(f"W{index}", WaterUseType.DOMESTIC, 100 + index, occupants=2)
    engine = WaterConsumptionEngine()
    assert engine.annual_liters((use,)) == (100 + index) * 365
    assert engine.liters_per_person_day((use,)) == pytest.approx((100 + index) / 2)
