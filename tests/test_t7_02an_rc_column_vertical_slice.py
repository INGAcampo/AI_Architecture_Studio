import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.rc_column_vertical_slice import RCColumnVerticalSlice
    r=RCColumnVerticalSlice().run();assert r.result.status=='PASS' and '# Reinforced Concrete Column Design' in r.report.markdown
