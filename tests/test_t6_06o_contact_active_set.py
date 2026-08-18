import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.contact_active_set import ContactActiveSet
    assert ContactActiveSet().active((.1,-.1,0))==(1,2)
