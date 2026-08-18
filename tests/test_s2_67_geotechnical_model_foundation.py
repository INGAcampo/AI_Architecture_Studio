import pytest
from engines.structural.geotechnical import *

@pytest.mark.parametrize("index", range(120))
def test_geotechnical(index):
    layer = SoilLayer(f"L{index}", 2 + index*0.01, 18, 10, 30)
    stress = GeotechnicalModel().vertical_stress((layer,))
    assert stress > 0
