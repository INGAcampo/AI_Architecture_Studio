"""Public module supporting the sixth Omega integrated product release."""
from pathlib import Path
from aias_omega_release4.workflow import build_bim_building
from aias_omega_release2.quantity import QuantityEngine
from .cost import CostCatalog,CostItem,BoqEngine
from .documents import DocumentationEngine
def build_and_export(output:Path):
    """Build the and export required by the sixth Omega integrated product release from explicit inputs."""
    project,info=build_bim_building()
    q=QuantityEngine()
    for wall_id in info["walls"]: q.attach_wall_quantity(project,wall_id,185.0)
    catalog=CostCatalog()
    catalog.add(CostItem("CONC-WALL","Concrete walls","m3",185.0))
    catalog.add(CostItem("CONC-SLAB","Concrete slab","m3",170.0))
    lines=BoqEngine().from_bim(project,catalog)
    output.mkdir(parents=True,exist_ok=True)
    d=DocumentationEngine()
    paths={"csv":output/"boq.csv","json":output/"boq.json","md":output/"summary.md"}
    d.export_boq_csv(lines,paths["csv"]); d.export_boq_json(lines,paths["json"]); d.export_summary_md(project,lines,paths["md"])
    return project,lines,paths
