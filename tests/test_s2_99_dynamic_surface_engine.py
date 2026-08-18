import pytest
from engines.civil.dynamic_surfaces import *

@pytest.mark.parametrize("i", range(120))
def test_surface(i):
    s = DynamicSurface((
        SurfacePoint(0,0,100+i),
        SurfacePoint(1,0,101+i),
        SurfacePoint(0,1,99+i),
    ))
    assert s.average_elevation() == pytest.approx(100+i)
    updated = s.update_point(0, SurfacePoint(0,0,102+i))
    assert updated.points[0].z == 102+i
