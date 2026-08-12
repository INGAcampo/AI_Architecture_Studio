import pytest
from engines.structural.systems.slabs import *

@pytest.mark.parametrize("i",range(120))
def test_slab(i):
    s=StructuralSlab(f"S{i}",StructuralSlabType("ST","Slab",0.2,"CONC"),((0,0),(6,0),(6,4),(0,4)),(((2,1),(3,1),(3,2),(2,2)),))
    e=StructuralSlabEngine();q=e.quantities(s)
    assert q.gross_area==pytest.approx(24)
    assert q.net_area==pytest.approx(23)
    assert q.volume==pytest.approx(4.6)
    assert e.validate(s)==()
