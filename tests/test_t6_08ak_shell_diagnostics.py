import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.shell_diagnostics import ShellDiagnosticsEngine
    assert not ShellDiagnosticsEngine().inspect(True,.5,2).warnings
