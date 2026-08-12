import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.principal_stress import PrincipalStress
    assert PrincipalStress().plane(10,0,0)==(10.0,0.0)
