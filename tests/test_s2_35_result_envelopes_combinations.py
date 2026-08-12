import pytest
from engines.structural.envelopes import *

@pytest.mark.parametrize("index", range(120))
def test_envelopes(index):
    engine = ResultEnvelopeEngine()
    samples = (
        ResultSample("A","O",float(index)),
        ResultSample("B","O",float(-index-1)),
    )
    env = engine.envelope(samples)
    assert env["minimum"].value <= env["maximum"].value
    assert engine.weighted_sum(samples,{"A":1.2,"B":0.5}) == pytest.approx(1.2*index - 0.5*(index+1))
