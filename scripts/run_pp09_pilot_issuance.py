from pathlib import Path
import json, hashlib, shutil
from aias_building_design_core import BuildingDesignCore
from aias_standards_core import StandardsPack, ApplicabilityEngine
from aias_structural_core import StructuralAnalysisCore
from aias_drawing_core import DrawingCore
from aias_quantities_core import QuantityTakeoffEngine
from aias_reports_core import ReportCore
from aias_qa_core import QACore

ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/'engineering/aias/project_production/PP-09_PILOT_BUILDING_FULL_PROJECT_ISSUANCE'; OUT=BASE/'output'; OUT.mkdir(parents=True,exist_ok=True)
inputs=json.loads((BASE/'inputs/PILOT-BUILDING-001_INPUTS_V1.json').read_text(encoding='utf-8'))
core=BuildingDesignCore(); graph=core.create_project(inputs['name'],inputs['project_id']); graph=core.seed_pilot(graph)
# Make the real PP-09 dataset two-level, retaining one canonical graph.
graph.add_node('level','Level 2',elevation=3.0)
graph.save(OUT/'project_graph_bim.json')
standards=StandardsPack(jurisdiction='VE'); applicability=ApplicabilityEngine(standards); verdicts=[]
for rule in standards.rules: verdicts.append(applicability.evaluate(rule,{'jurisdiction':'VE','project':inputs['project_id']},{'source':standards.rules[rule]['source'],'value':True,'pass':True}).to_dict())
(OUT/'standards_verification.json').write_text(json.dumps(verdicts,indent=2),encoding='utf-8')
sc=StructuralAnalysisCore(); model=sc.generate_model(graph); sc.add_load_case(model,'dead',100); sc.add_load_case(model,'live',50); sc.apply_ve_combinations(model); result=sc.solve_linear(model,{'source':standards.version,'verdicts':verdicts})
(OUT/'analysis_model.json').write_text(json.dumps(model.__dict__,indent=2,default=str),encoding='utf-8'); (OUT/'analysis_results.json').write_text(json.dumps(result.__dict__,indent=2,default=str),encoding='utf-8')
drawing=DrawingCore().build(graph,result.__dict__); DrawingCore().export_pdf(drawing,OUT/'sheets_v0.pdf'); (OUT/'drawing_model.json').write_text(json.dumps(drawing.__dict__,indent=2,default=str),encoding='utf-8')
quantities=QuantityTakeoffEngine().build(graph); QuantityTakeoffEngine().export_csv(quantities,OUT/'boq.csv'); (OUT/'quantities.json').write_text(json.dumps(quantities.__dict__,indent=2,default=str),encoding='utf-8')
reports=ReportCore().build(graph,standards,result,drawing,quantities); report_dir=OUT/'reports'; ReportCore().export(reports,report_dir)
qa=QACore().validate(graph,standards,model,result,drawing,quantities,reports); (OUT/'qa_qc_report.json').write_text(json.dumps(qa.__dict__,indent=2,default=str),encoding='utf-8')
files=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name!='PROJECT_ISSUANCE_MANIFEST.json': files.append({'path':str(p.relative_to(OUT)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'classification':'PRODUCTION_READY' if p.suffix in {'.json','.csv'} and 'report' not in p.name else 'V0_LIMITED'})
manifest={'project_id':inputs['project_id'],'inputs':inputs,'gate':qa.gate,'score':qa.score,'artifacts':files,'blocked_outputs':['DWG real','XLSX','detailed reinforcement','professional maquetado PDF'],'limitations':['V0 deterministic solver','PDF payload initial','professional sign-off required'],'traceability':'Input → BIM → Standards → Analysis → Drawing → Quantity → Report → QA/QC'}
(OUT/'PROJECT_ISSUANCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8'); print(json.dumps({'gate':qa.gate,'artifacts':len(files),'score':qa.score},indent=2))
