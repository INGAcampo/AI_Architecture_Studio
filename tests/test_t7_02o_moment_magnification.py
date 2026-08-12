import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.moment_magnification import Engine
    assert Engine().calculate(1,2,3)==6
