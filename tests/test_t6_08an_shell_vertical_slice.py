import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.shell_vertical_slice import ShellVerticalSlice
    r=ShellVerticalSlice().run();assert len(r.layers)==3 and '# Advanced Shells' in r.report.markdown
