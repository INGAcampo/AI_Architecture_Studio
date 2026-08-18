import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem2d.fem2d_vertical_slice import Fem2DVerticalSlice
    r=Fem2DVerticalSlice().run(2,1,2,1,(.02,.04),125,.85)
    assert len(r.nodes)==6 and '# Advanced 2D FEM' in r.report.markdown
