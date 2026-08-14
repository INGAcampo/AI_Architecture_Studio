from pathlib import Path
from aias_building_design_core import BuildingDesignCore
from aias_cad_professional import CADEngine
import json
root=Path(__file__).resolve().parents[1]; out=root/'engineering/aias/professional_project_production/PRO-02_PROFESSIONAL_CAD_DRAWING_ENGINE/PILOT-BUILDING-001_CAD_V0.json'; out.parent.mkdir(parents=True,exist_ok=True)
g=BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project('Edificación piloto AIAS Venezuela')); d=CADEngine().build(g,{}); out.write_text(CADEngine().serialize(d),encoding='utf-8'); print(json.dumps({'views':len(d.views),'sheets':len(d.sheets),'entities':len(d.entities),'errors':CADEngine().validate(d)}))
