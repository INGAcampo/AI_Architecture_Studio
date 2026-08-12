import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.shell_domain import ShellLayer
    assert ShellLayer('M',.1,0).thickness==pytest.approx(.1)
