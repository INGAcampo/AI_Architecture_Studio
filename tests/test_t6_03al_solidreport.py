import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.solidreport import SolidReportEngine
    assert '3D Solid FEM' in SolidReportEngine().build(4,1,100).markdown
