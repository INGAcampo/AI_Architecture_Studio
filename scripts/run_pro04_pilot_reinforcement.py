from pathlib import Path
import json
from aias_building_design_core import BuildingDesignCore
from aias_structural_professional import ProfessionalStructuralEngine
from aias_reinforcement_detailing import ReinforcementEngine
root=Path(__file__).resolve().parents[1]; out=root/'engineering/aias/professional_project_production/PRO-04_REINFORCEMENT_DETAILING_ENGINE/PILOT-BUILDING-001_REINFORCEMENT_V0.json'
g=BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project('Edificación piloto AIAS Venezuela')); g.add_node('beam','Beam B1'); g.add_node('column','Column C1')
s=ProfessionalStructuralEngine(); m=s.generate_3d_model(g); s.add_loads(m); s.apply_combinations(m); r=s.analyze_and_design(m,{'pack':'VE-PILOT-001.0'})
e=ReinforcementEngine(); re=e.build(r,{'pack':'VE-PILOT-001.0','constructive_detailing':False}); payload={'reinforcement':re.__dict__,'cad_details':e.cad_details(re),'total_steel_kg':e.total_steel_kg(re)}; out.write_text(json.dumps(payload,indent=2,default=str),encoding='utf-8'); print(json.dumps({'bar_sets':len(re.bar_sets),'steel_kg':payload['total_steel_kg'],'findings':len(re.findings)}))
