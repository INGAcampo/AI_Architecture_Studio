import pytest
from engines.analysis.benchmarks import *

@pytest.mark.parametrize("i",range(120))
def test_benchmark(i):
    s=EngineeringBenchmarkSuite()
    u=s.axial_bar_displacement(1000,2,0.01,200e9)
    assert u==pytest.approx(1e-6)
    r=s.compare("axial",1e-6,u,1e-9)
    assert r.passed
