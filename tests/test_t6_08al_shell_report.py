import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.shell_report import ShellReportEngine
    assert 'Advanced Shells' in ShellReportEngine().build(3,.006,.5,2).markdown
