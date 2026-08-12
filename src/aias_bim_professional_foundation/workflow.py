"""Public module supporting professional BIM foundation modeling and exchange."""
import json
from pathlib import Path
from uuid import uuid4
from .core import Point2D,Material,Level,GridLine
from .walls import Wall
from .project import BimProject,Opening
from .engines import QuantityEngine,AnalyticalEngine
from .io import Serializer,IfcLiteExporter

def build_demo(out):
    """Build the demo required by professional BIM foundation modeling and exchange from explicit inputs."""
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    p=BimProject("AIAS BIM Foundation Demo")
    p.add_material(Material("CONC30","Concrete 30 MPa","concrete",2400,{"E_MPa":30000}))
    p.add_level(Level("L0","Ground Floor",0))
    p.add_grid(GridLine("GA","A",Point2D(0,0),Point2D(0,10)))
    p.add_grid(GridLine("G1","1",Point2D(0,0),Point2D(12,0)))
    w=Wall(Point2D(0,0),Point2D(8,0),3.2,0.2,"L0","CONC30","Wall W01")
    p.add_wall(w)
    p.add_opening(Opening(w.wall_id,1.0,2.1,0.0,"door","Door D01",uuid4().hex))
    p.add_opening(Opening(w.wall_id,1.5,1.2,0.9,"window","Window W01",uuid4().hex))
    q=QuantityEngine().wall(p,w.wall_id)
    a=AnalyticalEngine().wall(w)
    project_path=out/"bim_foundation_project.aiasbim.json"
    Serializer().save(p,project_path)
    ifc_path=out/"wall_ifc_lite.json"
    ifc_path.write_text(json.dumps(IfcLiteExporter().wall(w,q),indent=2),encoding="utf-8")
    return p,w,q,a,project_path,ifc_path
