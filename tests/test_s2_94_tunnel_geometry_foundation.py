import pytest
from engines.civil.tunnels import *
@pytest.mark.parametrize("i",range(120))
def test_tunnel(i):
    t=CircularTunnel(f"T{i}",8,500);e=TunnelGeometryEngine()
    assert e.excavation_area(t)>0 and e.excavation_volume(t)>0 and e.lining_area(t)>0
