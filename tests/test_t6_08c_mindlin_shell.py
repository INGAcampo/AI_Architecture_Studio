import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.mindlin_shell import MindlinShellEngine
    assert MindlinShellEngine().bending_rigidity(30e9,.2)>0
