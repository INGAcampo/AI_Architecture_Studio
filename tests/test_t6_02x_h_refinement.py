import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem2d.h_refinement import HRefinementEngine
    assert abs(HRefinementEngine().target_size(1,.2,.05)-.5)<1e-12
