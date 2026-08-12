"""Public module supporting professional BIM foundation modeling and exchange."""
import json
from dataclasses import asdict
from pathlib import Path
from uuid import uuid4
from .core import Point2D,Material,Level,GridLine
from .walls import Wall
from .project import BimProject,Opening

class Serializer:
    """Execute the public Serializer operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    def save(self,p,path):
        """Persist save for professional BIM foundation modeling and exchange in its stable external representation."""
        data={
            "name":p.name,
            "materials":[asdict(m) for m in p.materials.values()],
            "levels":[asdict(l) for l in p.levels.values()],
            "grids":[{"grid_id":g.grid_id,"name":g.name,"start":[g.start.x,g.start.y],"end":[g.end.x,g.end.y]} for g in p.grids.values()],
            "walls":[{"wall_id":w.wall_id,"name":w.name,"start":[w.start.x,w.start.y],"end":[w.end.x,w.end.y],
                      "height_m":w.height_m,"thickness_m":w.thickness_m,"level_id":w.level_id,
                      "material_id":w.material_id,"revision":w.revision} for w in p.walls.values()],
            "openings":[asdict(o) for o in p.openings.values()],
        }
        Path(path).write_text(json.dumps(data,indent=2),encoding="utf-8")

    def load(self,path):
        """Load load for professional BIM foundation modeling and exchange while preserving typed state."""
        d=json.loads(Path(path).read_text(encoding="utf-8")); p=BimProject(d["name"])
        for x in d["materials"]: p.add_material(Material(**x))
        for x in d["levels"]: p.add_level(Level(**x))
        for x in d["grids"]: p.add_grid(GridLine(x["grid_id"],x["name"],Point2D(*x["start"]),Point2D(*x["end"])))
        for x in d["walls"]:
            w=Wall(Point2D(*x["start"]),Point2D(*x["end"]),x["height_m"],x["thickness_m"],x["level_id"],x["material_id"],x["name"],x["wall_id"])
            w.revision=x["revision"]; p.add_wall(w)
        for x in d["openings"]: p.add_opening(Opening(**x))
        return p

class IfcLiteExporter:
    """Execute the public IfcLiteExporter operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    def wall(self,w,q):
        """Execute the public IfcLiteExporter.wall operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
        return {"ifc_class":"IfcWall","global_id":w.wall_id,"name":w.name,
                "axis":[[w.start.x,w.start.y],[w.end.x,w.end.y]],
                "height_m":w.height_m,"thickness_m":w.thickness_m,
                "GrossArea":q.gross_area_m2,"NetArea":q.net_area_m2,"NetVolume":q.net_volume_m3}
