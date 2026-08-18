import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.hpc_domain import Partition
    assert Partition(0,('E1',),1).estimated_cost==1
