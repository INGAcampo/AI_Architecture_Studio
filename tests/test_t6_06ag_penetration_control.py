import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.penetration_control import PenetrationControlEngine
    assert PenetrationControlEngine().penalty_update(100,1e-3,1e-4)==200
