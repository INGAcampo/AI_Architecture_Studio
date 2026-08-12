import pytest
from bim_authoring.railings import *

@pytest.mark.parametrize("i", range(120))
def test_railing(i):
    railing = RailingInstance(
        f"R{i}",
        RailingType("RT","Steel",1.05,1.0,"steel"),
        ((0,0,0),(3,0,0),(3,4,0)),
    )
    engine = NativeBimRailingEngine()
    q = engine.quantities(railing)
    assert q.path_length == pytest.approx(7)
    assert q.post_count == 8
    assert engine.validate(railing) == ()
