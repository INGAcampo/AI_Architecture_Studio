import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.short_term_deflection import ShortTermDeflectionEngine
    assert ShortTermDeflectionEngine().simply_supported_uniform(10,6000,25000,1e9)>0
