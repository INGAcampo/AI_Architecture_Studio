import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.shell_domain import ShellLayer
    from analysis.shells.laminate_stack import LaminateStack
    assert LaminateStack().total_thickness((ShellLayer('M',.1,0),ShellLayer('M',.2,0)))==pytest.approx(.3)
