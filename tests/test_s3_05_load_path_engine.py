import pytest
from engines.structural.systems.load_paths import *

@pytest.mark.parametrize("i",range(120))
def test_load_path(i):
    e=LoadPathEngine()
    e.add_transfer(LoadTransfer("SLAB","B1",0.5));e.add_transfer(LoadTransfer("SLAB","B2",0.5));e.add_transfer(LoadTransfer("B1","C1",1.0))
    assert e.distribute("SLAB",100)==(("B1",50.0),("B2",50.0))
    assert e.path_exists("SLAB","C1")
