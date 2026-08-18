import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.reaction_recovery import ReactionRecoveryEngine
    assert ReactionRecoveryEngine().recover(((2,0),(0,4)),(2,2),(4,8))==(0,0)
