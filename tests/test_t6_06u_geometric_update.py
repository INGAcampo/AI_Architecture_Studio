import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.geometric_update import GeometricUpdateEngine
    assert GeometricUpdateEngine().update(((0,0),),((1,2),))==((1,2),)
