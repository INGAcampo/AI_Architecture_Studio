import pytest
from engines.structural.systems.foundations import *

@pytest.mark.parametrize("i",range(120))
def test_foundation(i):
    f=FoundationElement(f"F{i}",FoundationKind.ISOLATED,2,2,0.5,"CONC",("C1",))
    e=FoundationEngine();q=e.quantities(f)
    assert q.area==pytest.approx(4)
    assert q.volume==pytest.approx(2)
    assert e.bearing_pressure(f,800)==pytest.approx(200)
    assert e.validate(f)==()
