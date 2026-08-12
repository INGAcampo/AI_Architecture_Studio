import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.stick_slip_state import Engine
    assert Engine().calculate(1,2,3)==6
