from pathlib import Path
import hashlib, json, subprocess, os
from types import SimpleNamespace
from aias_building_design_core import BuildingDesignCore
from aias_standards_core import StandardsPack
from aias_structural_professional import ProfessionalStructuralEngine
from aias_reinforcement_detailing import ReinforcementEngine
from aias_cad_professional import CADEngine
from aias_quantities_core import QuantityTakeoffEngine
from aias_reports_core import ReportCore
from aias_qa_core import QACore
from aias_regeneration import RegenerationEngine
root=Path(__file__).resolve().parents[1]; base=root/'engineering/aias/professional_project_production/PRO-06_FULL_DOWNSTREAM_REGENERATION'; out=base/'PILOT-BUILDING-001_REGENERATION_JOURNAL.json'
c=BuildingDesignCore(); before=c.seed_pilot(c.create_project('Edificación piloto AIAS Venezuela')); after=c.seed_pilot(c.create_project('Edificación piloto AIAS Venezuela'))
material=next(n for n in after.nodes if n['type']=='material'); material['properties']['grade']='C30/37' # controlled material change
e=RegenerationEngine(); plan=e.plan(before,after,{})
standards=StandardsPack(); s=ProfessionalStructuralEngine(); model=s.generate_3d_model(after); s.add_loads(model); s.apply_combinations(model); structural=s.analyze_and_design(model,{'pack':'VE-PILOT-001.0'}); reinforcement=ReinforcementEngine().build(structural,{'pack':'VE-PILOT-001.0','constructive_detailing':False}); cad=CADEngine().build(after,structural.__dict__); q=QuantityTakeoffEngine().build(after)
# Explicit compatibility adapter: advanced envelopes/checks are projected into the PP-07 read contract.
report_result=SimpleNamespace(status=structural.status,internal_forces={k:v['M_kNm'] for k,v in structural.load_envelopes.items()},code_checks={k:v['status'] for k,v in structural.design_checks.items()},reactions={},displacements={},drifts={k:v['drift_ratio'] for k,v in structural.load_envelopes.items()},evidence_sha256=structural.evidence_sha256)
reports=ReportCore().build(after,standards,report_result,cad,q); qa=QACore().validate(after,standards,model,report_result,cad,q,reports)
runners={'standards':lambda:{'pack':standards.version},'analysis':lambda:structural.__dict__,'reinforcement':lambda:reinforcement.__dict__,'cad':lambda:cad.__dict__,'quantities':lambda:q.__dict__,'xlsx':lambda:{'regenerated_by':'PRO05 workbook pipeline','input_graph_sha':plan['graph_after']},'reports':lambda:reports.__dict__,'qa_qc':lambda:qa.__dict__,'issuance_manifest':lambda:{'gate':qa.gate,'graph_sha':plan['graph_after']}}
result=e.execute(plan,runners); payload={'change':{'element_id':material['id'],'property':'grade','before':'C25/30','after':'C30/37'},'plan':plan,'result':result,'qa_gate':qa.gate,'reinforcement_classification':'PRELIMINARY'}; out.write_text(json.dumps(payload,indent=2,default=str),encoding='utf-8'); print(json.dumps({'status':result['status'],'regenerated':len(result['journal']),'qa_gate':qa.gate},indent=2))
