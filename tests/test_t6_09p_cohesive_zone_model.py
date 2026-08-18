import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.cohesive_zone_model import CohesiveZoneModel
    assert CohesiveZoneModel().traction(.01,1000,.2)==pytest.approx(8)
