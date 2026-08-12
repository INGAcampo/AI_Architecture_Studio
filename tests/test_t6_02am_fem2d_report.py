import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem2d.fem2d_report import Fem2DReportEngine
    assert 'Advanced 2D FEM' in Fem2DReportEngine().build(4,1,100,.05,True).markdown
