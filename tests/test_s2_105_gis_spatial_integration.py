import pytest
from engines.civil.gis_integration import *

@pytest.mark.parametrize("i", range(120))
def test_gis(i):
    features = (
        GeoFeature("A",-66,10,{"type":"road"}),
        GeoFeature("B",-65,11,{"type":"bridge"}),
    )
    e = GisSpatialIntegration()
    assert e.bbox(features) == (-66,10,-65,11)
    assert e.find_by_property(features,"type","road")[0].feature_id == "A"
