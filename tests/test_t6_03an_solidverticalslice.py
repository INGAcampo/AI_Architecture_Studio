import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.solidverticalslice import SolidVerticalSlice
    r=SolidVerticalSlice().run()
    assert r.volume>0 and '# 3D Solid FEM Analysis Report' in r.report.markdown
