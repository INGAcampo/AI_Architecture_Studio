import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.serviceability_check import ServiceabilityCheckEngine
    assert ServiceabilityCheckEngine().check(5,10,.2,.3)
