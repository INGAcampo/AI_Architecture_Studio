from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True, slots=True)
class WallGeometry:
    wall_id: str
    vertices: tuple[tuple[float, float, float], ...]
    faces: tuple[tuple[int, ...], ...]
    length: float
    thickness: float
    height: float

class WallGeometryBuilder:
    def build(self, wall):
        sx, sy, sz = wall.profile.start
        ex, ey, ez = wall.profile.end
        dx, dy = ex - sx, ey - sy
        length = hypot(dx, dy)
        nx, ny = -dy / length, dx / length
        half = wall.wall_type.structure.total_thickness / 2.0
        z0 = wall.profile.base_elevation
        z1 = z0 + wall.profile.height

        a = (sx + nx*half, sy + ny*half, z0)
        b = (ex + nx*half, ey + ny*half, z0)
        c = (ex - nx*half, ey - ny*half, z0)
        d = (sx - nx*half, sy - ny*half, z0)
        a2 = (a[0], a[1], z1)
        b2 = (b[0], b[1], z1)
        c2 = (c[0], c[1], z1)
        d2 = (d[0], d[1], z1)

        return WallGeometry(
            wall.wall_id,
            (a,b,c,d,a2,b2,c2,d2),
            (
                (0,1,2,3),
                (4,7,6,5),
                (0,4,5,1),
                (1,5,6,2),
                (2,6,7,3),
                (3,7,4,0),
            ),
            length,
            wall.wall_type.structure.total_thickness,
            wall.profile.height,
        )
