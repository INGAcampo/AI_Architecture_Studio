import pytest
from engines.structural.loads import *
@pytest.mark.parametrize("index", range(120))
def test_load_engine(index):
    engine=LoadEngine()
    load=NodalLoad(f"L{index}","N1",LoadKind.DEAD,fx=index,fy=2*index,fz=-index)
    engine.add(load)
    assert load.magnitude >= 0
    assert engine.resultant("N1") == (index,2*index,-index)
