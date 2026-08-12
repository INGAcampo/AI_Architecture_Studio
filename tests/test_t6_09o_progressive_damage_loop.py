import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.progressive_damage_loop import ProgressiveDamageLoop
    assert ProgressiveDamageLoop().run(.8).converged
