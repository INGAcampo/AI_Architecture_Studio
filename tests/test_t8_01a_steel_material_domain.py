import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_library.steel_material_domain import SteelMaterial
    m=SteelMaterial('X','S',345,450)
    assert m.shear_modulus_mpa>0
