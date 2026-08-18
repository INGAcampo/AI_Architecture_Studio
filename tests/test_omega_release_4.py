import pytest
from aias_omega_release4.workflow import build_bim_building
from aias_omega_release4.quantities import BimQuantityService

@pytest.mark.parametrize("i", range(200))
def test_bim_building(i):
    p,info=build_bim_building()
    types={o.object_type for o in p.objects.values()}
    assert {"bim_level","bim_wall","bim_slab","bim_door","bim_window"} <= types
    assert len(p.objects)==8
    assert len(p.graph.all())==7
    assert info["net_wall_volume_m3"]>0

@pytest.mark.parametrize("i", range(100))
def test_opening_reduces_quantity(i):
    p,info=build_bim_building()
    south=info["walls"][0]
    wall=p.objects[south]
    gross=wall.properties["length_m"]*wall.properties["height_m"]
    net=BimQuantityService().wall_net_area(p,south)
    assert net < gross
    assert gross-net == pytest.approx(2.1)
