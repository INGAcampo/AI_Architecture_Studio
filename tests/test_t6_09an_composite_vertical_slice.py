import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.composite_vertical_slice import CompositeVerticalSlice
    r=CompositeVerticalSlice().run();assert r.result.converged and '# Progressive Composite Damage' in r.report.markdown
