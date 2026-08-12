import pytest
from engines.geotechnical.stratigraphy import *
@pytest.mark.parametrize("i",range(120))
def test_stratigraphy(i):
    m=SoilMaterial(f"M{i}","Soil",18,10,30,25000)
    p=SoilProfile(f"P{i}",(SoilLayer("L1",0,2,m),SoilLayer("L2",2,5,m)))
    assert p.layer_at(1).layer_id=="L1" and p.total_depth==5
