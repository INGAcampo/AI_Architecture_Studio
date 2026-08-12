import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.concrete_material import ConcreteMaterial
    assert ConcreteMaterial('C',25).elastic_modulus()>0
