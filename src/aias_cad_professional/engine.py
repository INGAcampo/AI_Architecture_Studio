from __future__ import annotations
from dataclasses import dataclass, field, asdict
import hashlib, json

@dataclass
class CADDocument:
    project_id: str
    layers: list[dict] = field(default_factory=list)
    entities: list[dict] = field(default_factory=list)
    views: list[dict] = field(default_factory=list)
    sheets: list[dict] = field(default_factory=list)
    schema: str = "aias.cad_intermediate.v1"

class CADEngine:
    """BIM-derived CAD intermediate; deterministic and serializable, DWG-neutral."""
    def build(self, graph, analysis_results=None) -> CADDocument:
        if not graph.nodes: raise ValueError("CAD generation requires Project Graph")
        doc=CADDocument(graph.project_id)
        doc.layers=[{"name":"A-WALL","color":7,"lineweight":0.35},{"name":"A-DOOR","color":3,"lineweight":0.25},{"name":"S-STRUCT","color":1,"lineweight":0.50},{"name":"A-DIMS","color":2,"lineweight":0.18},{"name":"A-TEXT","color":7,"lineweight":0.18},{"name":"A-GRID","color":8,"lineweight":0.13}]
        def add(kind, layer, source, geometry, **extra):
            payload={"id":f"cad-{len(doc.entities)+1:04d}","kind":kind,"layer":layer,"source_node_id":source,"geometry":geometry,"attributes":extra}; payload["sha256"]=sha(payload); doc.entities.append(payload)
        for node in graph.nodes:
            t=node["type"]; p=node.get("properties",{}); sid=node["id"]
            if t=="wall": add("polyline","A-WALL",sid,[[0,0],[4,0],[4,0.2],[0,0.2],[0,0]],closed=True)
            elif t=="door": add("block","A-DOOR",sid,[[0,0],[0.9,0]],block_name="DOOR_SINGLE")
            elif t=="window": add("block","A-DOOR",sid,[[0,0],[1.2,0]],block_name="WINDOW")
            elif t in {"column","beam","slab","foundation"}: add("rectangle","S-STRUCT",sid,[[0,0],[0.3,0.3]],structural_type=t)
            elif t=="grid": add("line","A-GRID",sid,[[0,-2],[0,8]],axis=p.get("axis","A")); add("bubble","A-GRID",sid,[0,8],label=p.get("axis","A"))
            elif t=="level": add("level","A-TEXT",sid,[-2,0],elevation=p.get("elevation",0.0)); add("text","A-TEXT",sid,[0,0],text=node["name"],style="TITLE")
            elif t=="space": add("text","A-TEXT",sid,[2,2],text=node["name"],style="ROOM_TAG")
        for i, node in enumerate(graph.nodes):
            if node["type"] in {"wall","slab","foundation"}: add("dimension","A-DIMS",node["id"],[[0,0],[4,0]],value=4.0,dimension_type="linear")
        view_specs=[("A-101","Architectural Plan","plan"),("S-101","Structural Plan","plan"),("S-201","Foundation Plan","foundation"),("A-301","Building Section","section"),("A-401","Building Elevation","elevation")]
        for num,title,kind in view_specs:
            vid=f"view-{num}"; ids=[e["id"] for e in doc.entities]; doc.views.append({"id":vid,"number":num,"title":title,"kind":kind,"scale":"1:100","viewport":{"x":0,"y":0,"width":297,"height":210},"entity_ids":ids,"references":["ProjectGraph/BIM"]}); doc.sheets.append({"id":f"sheet-{num}","number":num,"title":title,"view_id":vid,"scale":"1:100","title_block":{"project_id":graph.project_id,"revision":"V0"},"sha256":sha(doc.views[-1])})
        return doc

    def validate(self, doc: CADDocument) -> list[str]:
        errors=[]; layer_names={l["name"] for l in doc.layers}
        if not doc.views or not doc.sheets: errors.append("views/sheets required")
        if any(e.get("layer") not in layer_names for e in doc.entities): errors.append("entity layer undefined")
        if any(v.get("scale") not in {"1:50","1:100","1:200"} for v in doc.views): errors.append("invalid scale")
        if any(not s.get("title_block") for s in doc.sheets): errors.append("title block missing")
        return errors

    def serialize(self, doc: CADDocument) -> str: return json.dumps(asdict(doc),indent=2,sort_keys=True)

def sha(value): return hashlib.sha256(json.dumps(value,sort_keys=True,default=str).encode()).hexdigest()
