import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.reaction_recovery import ReactionRecovery
    assert ReactionRecovery().recover(((2,0),(0,4)),(2,2),(4,8))==(0,0)
