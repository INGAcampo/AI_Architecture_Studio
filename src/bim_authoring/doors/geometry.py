from dataclasses import dataclass
from math import cos, sin, pi

@dataclass(frozen=True, slots=True)
class DoorGeometry:
    door_id: str
    frame_vertices: tuple[tuple[float, float, float], ...]
    panel_vertices: tuple[tuple[float, float, float], ...]
    swing_arc: tuple[tuple[float, float, float], ...]
    width: float
    height: float

class DoorGeometryBuilder:
    def build(self, door):
        width = door.door_type.width
        height = door.door_type.height
        t = door.door_type.panel.thickness
        x0 = door.offset
        x1 = x0 + width
        z0 = door.sill_height
        z1 = z0 + height

        frame = (
            (x0, 0, z0),
            (x1, 0, z0),
            (x1, 0, z1),
            (x0, 0, z1),
        )

        panel = (
            (x0, -t/2, z0),
            (x1, -t/2, z0),
            (x1, t/2, z1),
            (x0, t/2, z1),
        )

        arc = ()
        if door.door_type.operation.value in {"single_swing", "double_swing"}:
            radius = width
            points = []
            for step in range(7):
                angle = (pi/2) * step / 6
                x = x0 + radius * cos(angle)
                y = radius * sin(angle)
                points.append((x, y, z0))
            arc = tuple(points)

        return DoorGeometry(
            door.door_id,
            frame,
            panel,
            arc,
            width,
            height,
        )
