import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.domain_partition import DomainPartitionEngine
    assert len(DomainPartitionEngine().partition(('E1','E2','E3'),2))==2
