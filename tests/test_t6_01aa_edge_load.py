import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.edge_load import Engine
    assert Engine().calculate(1,2,3)==6
