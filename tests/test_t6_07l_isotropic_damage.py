import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.isotropic_damage import IsotropicDamageEngine
    assert IsotropicDamageEngine().degrade((10,),.2)==pytest.approx((8,))
