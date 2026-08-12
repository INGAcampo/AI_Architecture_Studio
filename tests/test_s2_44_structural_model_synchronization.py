import pytest
from engines.structural.synchronization import *
@pytest.mark.parametrize("index",range(120))
def test_sync(index):
    r=StructuralModelSynchronizer().decide(f"O{index}",index+1,index)
    assert r.action is SyncAction.UPDATE
