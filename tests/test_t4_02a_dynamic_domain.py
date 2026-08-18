import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.dynamic_domain import ModalMode
    assert ModalMode(1,4,1,1,(1,)).mode_number==1
