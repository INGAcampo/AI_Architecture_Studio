import pytest
from design.steel.connection_domain import *
@pytest.mark.parametrize("i",range(120))
def test_domain(i):
    c=SteelConnection(f"C{i}",ConnectionFamily.SHEAR,ConnectionMethod.BOLTED,"W14X38","W14X38",ConnectionDemand(shear=100e3))
    assert c.demand.shear==pytest.approx(100e3)
