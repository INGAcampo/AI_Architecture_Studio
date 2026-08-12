import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.moment_curvature import MomentCurvatureEngine
    assert MomentCurvatureEngine().curvature(.003,100)>0
