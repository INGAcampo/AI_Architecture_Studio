import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.state_variable_manager import Engine
    assert Engine().calculate(1,2,3)==6
