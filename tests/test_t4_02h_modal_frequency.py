import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.modal_frequency import ModalFrequencyEngine
    assert ModalFrequencyEngine().from_eigenvalue(4)[0]==2
