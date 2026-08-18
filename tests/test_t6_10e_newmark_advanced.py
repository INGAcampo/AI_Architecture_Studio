import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.newmark_advanced import NewmarkAdvancedEngine
    assert len(NewmarkAdvancedEngine().step(0,0,0,1,1,0,10,.1))==3
