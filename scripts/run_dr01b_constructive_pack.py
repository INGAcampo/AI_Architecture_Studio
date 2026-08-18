from pathlib import Path
import json
from aias_constructive_standards import ConstructivePackValidator
from aias_building_design_core import BuildingDesignCore
from aias_structural_professional import ProfessionalStructuralEngine
from aias_reinforcement_detailing import ReinforcementEngine
root=Path(__file__).resolve().parents[1]; base=root/'engineering/aias/standards/VE_CONSTRUCTIVE_CONCRETE_PACK'; pack=json.loads((base/'VE_CONSTRUCTIVE_CONCRETE_PACK_1.0.json').read_text(encoding='utf-8'))
errors=ConstructivePackValidator().validate(pack)
if errors: raise ValueError(errors)
g=BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project('Edificación piloto AIAS Venezuela')); g.add_node('beam','Beam B1'); g.add_node('column','Column C1')
s=ProfessionalStructuralEngine(); m=s.generate_3d_model(g); s.add_loads(m); s.apply_combinations(m); result=s.analyze_and_design(m,{'pack':pack['version']}); r=ReinforcementEngine().build(result,{'pack':pack['version'],'constructive_detailing':False})
payload={'pack_version':pack['version'],'validation_errors':errors,'coverage':{'beam':'PARTIAL','column':'PARTIAL','slab':'INSUFFICIENT_EVIDENCE','foundation':'INSUFFICIENT_EVIDENCE'},'reinforcement_statuses':sorted(set(x['status'] for x in r.bar_sets)),'bar_sets':len(r.bar_sets),'findings':r.findings,'residual_blockers':pack['fail_closed_rules']}; (base/'DR01B_REINFORCEMENT_REEVALUATION.json').write_text(json.dumps(payload,indent=2,default=str),encoding='utf-8'); print(json.dumps(payload,indent=2,default=str))
