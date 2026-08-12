import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.mixed_mode_bk import BenzeggaghKenaneEngine
    assert BenzeggaghKenaneEngine().critical_energy(1,1,2,4,1)==pytest.approx(3)
