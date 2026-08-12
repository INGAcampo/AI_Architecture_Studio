import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.second_order_amplification import SecondOrderAmplification
    assert SecondOrderAmplification().b1(20,100)==pytest.approx(1.25)
