import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.long_term_deflection import LongTermDeflectionEngine
    assert LongTermDeflectionEngine().total(10,2)==30
