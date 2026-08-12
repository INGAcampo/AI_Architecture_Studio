import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.strain_compatibility import StrainCompatibilityEngine
    assert StrainCompatibilityEngine().steel_strain(100,500)>0
