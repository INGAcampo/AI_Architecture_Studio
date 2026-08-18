from pathlib import Path
import json
from aias_professional_qa import ProfessionalQAGate
root=Path(__file__).resolve().parents[1]; base=root/'engineering/aias/professional_project_production/PRO-07_PROFESSIONAL_PROJECT_QA_QC'
artifacts=[
 ('Project Graph/BIM','PRODUCTION_READY','PRO06 regeneration journal','PP-02/PRO-06',''),
 ('Standards/Analysis','PRODUCTION_READY','PRO01 structural evidence','PP-03/PRO-01',''),
 ('Reinforcement Model','PRELIMINARY','PRO04 certification','PRO-04','Verify constructive detailing standards'),
 ('CAD Intermediate','PRODUCTION_READY','PRO02 CAD model','PRO-02',''),
 ('DXF Exchange Set','V0_LIMITED','PRO03 export manifest','PRO-03','Adopt validated native DWG backend'),
 ('PDF Plan Set','V0_LIMITED','PRO03 export manifest','PRO-03','Implement professional PDF composition'),
 ('Native DWG','BLOCKED','PRO03 manifest','PRO-03','Install/integrate native DWG writer and roundtrip validation'),
 ('XLSX BOQ','V0_LIMITED','PRO05 workbook manifest','PRO-05','Implement in-process incremental refresh service'),
 ('Reports','PRODUCTION_READY','PP07 evidence','PP-07',''),
 ('Issuance/Regeneration','PRODUCTION_READY','PRO06 journal','PRO-06','')]
r=ProfessionalQAGate().evaluate(artifacts); (base/'EXECUTIVE_READINESS_MATRIX.json').write_text(json.dumps(r,indent=2),encoding='utf-8'); print(json.dumps({'verdict':r['verdict'],'score':r['score'],'findings':len(r['findings'])},indent=2))
