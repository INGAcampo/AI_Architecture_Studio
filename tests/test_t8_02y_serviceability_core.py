import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.serviceability_core import ServiceabilityEngine
    assert ServiceabilityEngine().deflection_limit_mm(3600)==10
