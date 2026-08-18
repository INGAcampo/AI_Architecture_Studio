import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.von_mises import VonMises
    assert VonMises().plane(10,0,0)==10
