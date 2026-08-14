from __future__ import annotations
import hashlib,json
from dataclasses import dataclass
from geometry_bim_bridge.contracts import BridgeGeometryPayload,BridgeMesh

@dataclass(frozen=True)
class RenderMeshPayload:
    entity_id:str
    entity_type:str
    global_id:str|None
    vertices:tuple
    triangles:tuple
    bounds_min:tuple
    bounds_max:tuple
    mesh_sha256:str
    metadata:dict

def canonical_mesh_sha256(mesh:BridgeMesh)->str:
    mesh.validate()
    data={"vertices":[list(map(float,v)) for v in mesh.vertices],"triangles":[list(map(int,t)) for t in mesh.triangles]}
    raw=json.dumps(data,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
    return hashlib.sha256(raw).hexdigest()

def build_render_payload(payload:BridgeGeometryPayload)->RenderMeshPayload:
    if payload.mesh is None:
        raise ValueError("bridge payload has no mesh")
    m=payload.mesh
    m.validate()
    xs=[v[0] for v in m.vertices]; ys=[v[1] for v in m.vertices]; zs=[v[2] for v in m.vertices]
    return RenderMeshPayload(
        payload.entity.entity_id,payload.entity.entity_type,payload.entity.global_id,
        m.vertices,m.triangles,
        (min(xs),min(ys),min(zs)),(max(xs),max(ys),max(zs)),
        canonical_mesh_sha256(m),dict(payload.metadata)
    )
