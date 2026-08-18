from __future__ import annotations
from typing import Any
def tessellate_box(record: dict[str, Any]) -> dict[str, Any]:
    """Create a deterministic preview mesh; not a B-Rep or engineering solid solver."""
    object_id=str(record.get("object_id", "")); params=record.get("geometry",{}).get("parameters",{})
    if not object_id.strip(): raise ValueError("object_id cannot be empty")
    h=float(params.get("height",0)); l=float(params.get("length",0)); t=float(params.get("thickness",0))
    if min(h,l,t) <= 0: raise ValueError("positive_box_dimensions_required")
    vertices=((0,0,0),(l,0,0),(l,t,0),(0,t,0),(0,0,h),(l,0,h),(l,t,h),(0,t,h))
    triangles=((0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),(1,5,6),(1,6,2),(2,6,7),(2,7,3),(3,7,4),(3,4,0))
    return {"object_id":object_id,"vertices":vertices,"triangles":triangles,"backend":"aias-deterministic-preview","engineering_brep":False}
