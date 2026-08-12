import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.contact_search import ContactSearchEngine
    assert ContactSearchEngine().candidate_pairs(((0,0),),((.1,0),),.2)==((0,0),)
