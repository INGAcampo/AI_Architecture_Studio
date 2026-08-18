import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.load_combination_design import LoadCombinationDesignEngine
    assert LoadCombinationDesignEngine().factored(10,5)==pytest.approx(20)
