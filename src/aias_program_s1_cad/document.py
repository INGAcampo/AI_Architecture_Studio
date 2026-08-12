"""Versioned CAD document JSON serialization and typed entity reconstruction."""
from __future__ import annotations
import json
from pathlib import Path
from .entities import Line, Circle, Arc, Polyline, Ellipse, Polygon
from .geometry import Point

class DocumentSerializer:
    """Persist layers, blocks, entities and annotations as a portable drawing document."""
    def save(self, entities, path: Path) -> None:
        """Persist save for the S1 professional CAD foundation program in its stable external representation."""
        rows=[]
        for e in entities:
            row={"id":e.entity_id,"layer":e.layer,"visible":e.visible,"locked":e.locked}
            if isinstance(e,Line):
                row.update(type="line",start=[e.start.x,e.start.y],end=[e.end.x,e.end.y])
            elif isinstance(e,Circle):
                row.update(type="circle",center=[e.center.x,e.center.y],radius=e.radius)
            elif isinstance(e,Arc):
                row.update(type="arc",center=[e.center.x,e.center.y],radius=e.radius,start_angle=e.start_angle,end_angle=e.end_angle)
            elif isinstance(e,Polyline):
                row.update(type="polyline",points=[[p.x,p.y] for p in e.points],closed=e.closed)
            elif isinstance(e,Ellipse):
                row.update(type="ellipse",center=[e.center.x,e.center.y],radius_x=e.radius_x,radius_y=e.radius_y)
            elif isinstance(e,Polygon):
                row.update(type="polygon",points=[[p.x,p.y] for p in e.points])
            rows.append(row)
        path.write_text(json.dumps({"version":1,"entities":rows},indent=2),encoding="utf-8")

    def load(self, path: Path):
        """Load load for the S1 professional CAD foundation program while preserving typed state."""
        data=json.loads(path.read_text(encoding="utf-8"))
        result=[]
        for row in data.get("entities",[]):
            common=dict(entity_id=row["id"],layer=row.get("layer","0"),visible=row.get("visible",True),locked=row.get("locked",False))
            t=row["type"]
            if t=="line": e=Line(**common,start=Point(*row["start"]),end=Point(*row["end"]))
            elif t=="circle": e=Circle(**common,center=Point(*row["center"]),radius=row["radius"])
            elif t=="arc": e=Arc(**common,center=Point(*row["center"]),radius=row["radius"],start_angle=row["start_angle"],end_angle=row["end_angle"])
            elif t=="polyline": e=Polyline(**common,points=[Point(*p) for p in row["points"]],closed=row.get("closed",False))
            elif t=="ellipse": e=Ellipse(**common,center=Point(*row["center"]),radius_x=row["radius_x"],radius_y=row["radius_y"])
            else: e=Polygon(**common,points=[Point(*p) for p in row["points"]])
            result.append(e)
        return result
