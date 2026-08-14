from __future__ import annotations
import hashlib
from dataclasses import dataclass
from geometry_bim_bridge.contracts import BridgeEntityRef

@dataclass(frozen=True)
class StableGeometryIdentity:
    semantic_key: str
    geometry_key: str
    composite_key: str

def make_geometry_identity(entity: BridgeEntityRef, geometry_sha256: str) -> StableGeometryIdentity:
    if len(geometry_sha256) != 64:
        raise ValueError("geometry_sha256 must be SHA256")
    raw="|".join((entity.source,entity.entity_type,entity.entity_id,entity.global_id or ""))
    semantic=hashlib.sha256(raw.encode("utf-8")).hexdigest()
    composite=hashlib.sha256((semantic+"|"+geometry_sha256).encode("ascii")).hexdigest()
    return StableGeometryIdentity(semantic,geometry_sha256,composite)
