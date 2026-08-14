from pathlib import Path
import json
from aias_building_design_core import BuildingDesignCore
from aias_structural_professional import ProfessionalStructuralEngine
root=Path(__file__).resolve().parents[1]
out=root/'engineering/aias/professional_project_production/PRO-01_STRUCTURAL_PROFESSIONALIZATION/PILOT-BUILDING-001_STRUCTURAL_V0.json'
g=BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project('Edificación piloto AIAS Venezuela'))
e=ProfessionalStructuralEngine(); m=e.generate_3d_model(g); e.add_loads(m); e.apply_combinations(m)
r=e.analyze_and_design(m,{'pack':'VE-PILOT-001.0'})
out.write_text(json.dumps(r.__dict__,indent=2,default=str),encoding='utf-8')
print(json.dumps({'status':r.status,'members':len(r.design_checks),'sha':r.evidence_sha256},indent=2))
