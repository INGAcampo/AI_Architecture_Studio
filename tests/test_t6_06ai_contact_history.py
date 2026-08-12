import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.contact_history import ContactHistory
    h=ContactHistory();h.add(1,'stick',10);assert h.latest()==(1,'stick',10)
