import pytest
from documentation_kernel.smart_dimensions import *

@pytest.mark.parametrize("i", range(120))
def test_dimension(i):
    engine = SmartDimensionEngine()
    d1 = engine.linear(f"D{i}", DimensionPoint(0, 0), DimensionPoint(3, 4), suffix=" m")
    d2 = engine.linear(f"D{i}-2", DimensionPoint(0, 0), DimensionPoint(6, 8))
    assert d1.measured_value == pytest.approx(5)
    assert d1.formatted() == "5.00 m"
    assert engine.chain_total((d1, d2)) == pytest.approx(15)
