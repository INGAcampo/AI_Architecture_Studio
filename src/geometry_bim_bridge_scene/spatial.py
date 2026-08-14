from __future__ import annotations

from dataclasses import dataclass

from geometry_bim_bridge_xform.transform import RigidTransform


@dataclass(frozen=True)
class SpatialPlacement:
    x_m: float = 0.0
    y_m: float = 0.0
    z_m: float = 0.0
    rz_degrees: float = 0.0


def compose_placements(parent: SpatialPlacement, child: SpatialPlacement) -> RigidTransform:
    import math

    angle=math.radians(parent.rz_degrees)
    c=math.cos(angle)
    s=math.sin(angle)

    cx=c*child.x_m-s*child.y_m
    cy=s*child.x_m+c*child.y_m

    return RigidTransform(
        tx=parent.x_m+cx,
        ty=parent.y_m+cy,
        tz=parent.z_m+child.z_m,
        rz_degrees=parent.rz_degrees+child.rz_degrees,
    )
