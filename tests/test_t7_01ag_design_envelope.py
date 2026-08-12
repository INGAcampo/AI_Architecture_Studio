import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.design_envelope import DesignEnvelopeEngine
    assert DesignEnvelopeEngine().maximum((-2,1))==-2
