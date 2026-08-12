import pytest
from engines.structural.sustainability import *

@pytest.mark.parametrize("index", range(120))
def test_sustainability(index):
    item = CarbonItem(
        f"C{index}",
        list(CarbonScope)[index % len(CarbonScope)],
        10 + index,
        2.5,
    )
    engine = SustainabilityCarbonEngine()
    assert item.emissions == pytest.approx((10 + index) * 2.5)
    assert engine.total_emissions((item,)) == pytest.approx(item.emissions)
    assert engine.carbon_intensity((item,), 100) > 0
