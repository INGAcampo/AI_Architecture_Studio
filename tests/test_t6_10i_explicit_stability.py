import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.explicit_stability import ExplicitStabilityEngine
    assert ExplicitStabilityEngine().stable(.1,.2)
