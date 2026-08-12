import pytest
from engines.structural.systems.bim_sync import *

@pytest.mark.parametrize("i",range(120))
def test_sync(i):
    e=BimStructuralSynchronization()
    r=e.synchronize({"B1":1,"B2":2},{"S1":1},{"B1":"S1","B2":"S2"})
    assert r.created==()
    assert r.updated==("B2",)
    assert r.unchanged==("B1",)
