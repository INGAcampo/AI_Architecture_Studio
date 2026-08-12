import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.memory_pool import Engine
    assert Engine().calculate(1,2,3)==6
