import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.shell_buckling import ShellBucklingEngine
    assert ShellBucklingEngine().factor(200,100)==2
