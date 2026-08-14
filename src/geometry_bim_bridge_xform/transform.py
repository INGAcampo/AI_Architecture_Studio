from __future__ import annotations

import math
from dataclasses import dataclass, replace

from geometry_bim_bridge.contracts import BridgeMesh
from geometry_bim_bridge_ext.render_payload import RenderMeshPayload, canonical_mesh_sha256


@dataclass(frozen=True)
class RigidTransform:
    tx: float = 0.0
    ty: float = 0.0
    tz: float = 0.0
    rz_degrees: float = 0.0


def transform_point(point, transform: RigidTransform):
    x, y, z = map(float, point)
    angle = math.radians(transform.rz_degrees)
    c = math.cos(angle)
    s = math.sin(angle)
    xr = c*x - s*y + transform.tx
    yr = s*x + c*y + transform.ty
    zr = z + transform.tz
    return (xr, yr, zr)


def transform_mesh(mesh: BridgeMesh, transform: RigidTransform) -> BridgeMesh:
    mesh.validate()
    out = BridgeMesh(
        vertices=tuple(transform_point(v, transform) for v in mesh.vertices),
        triangles=mesh.triangles,
    )
    out.validate()
    return out


def transform_render_payload(
    payload: RenderMeshPayload,
    transform: RigidTransform,
) -> RenderMeshPayload:
    mesh = BridgeMesh(
        vertices=payload.vertices,
        triangles=payload.triangles,
    )
    transformed = transform_mesh(mesh, transform)

    xs=[v[0] for v in transformed.vertices]
    ys=[v[1] for v in transformed.vertices]
    zs=[v[2] for v in transformed.vertices]

    return replace(
        payload,
        vertices=transformed.vertices,
        triangles=transformed.triangles,
        bounds_min=(min(xs),min(ys),min(zs)),
        bounds_max=(max(xs),max(ys),max(zs)),
        mesh_sha256=canonical_mesh_sha256(transformed),
    )
