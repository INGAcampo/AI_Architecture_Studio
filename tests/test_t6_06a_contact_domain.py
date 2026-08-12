import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.contact_domain import ContactPoint
    assert ContactPoint('S','M',-1e-6,(0,1),10,'stick').pressure==10
