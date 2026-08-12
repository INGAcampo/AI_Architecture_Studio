import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.benchmark_suite import BenchmarkSuite
    assert BenchmarkSuite().speedup(4,2)==2
