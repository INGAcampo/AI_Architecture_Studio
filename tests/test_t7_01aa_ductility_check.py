import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.ductility_check import DuctilityCheckEngine
    assert DuctilityCheckEngine().tension_controlled(.006)
