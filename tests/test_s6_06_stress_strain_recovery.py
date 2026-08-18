import pytest
from engines.analysis.stress_strain import *

@pytest.mark.parametrize("i",range(120))
def test_stress(i):
    r=StressStrainRecovery().axial(f"E{i}",100000,0.01,200e9)
    assert r.stress==pytest.approx(10e6)
    assert r.strain==pytest.approx(5e-5)
    assert StressStrainRecovery().utilization(r,250e6)==pytest.approx(0.04)
