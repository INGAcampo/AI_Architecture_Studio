import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.parallel_assembly import ParallelAssemblyEngine
    assert len(ParallelAssemblyEngine().assemble((((1,-1),(-1,1)),),((0,1),)))==4
