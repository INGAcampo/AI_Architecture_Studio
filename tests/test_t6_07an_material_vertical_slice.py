import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.material_vertical_slice import MaterialVerticalSlice
    r=MaterialVerticalSlice().run();assert r.state.yielded and '# Advanced Material Plasticity' in r.report.markdown
