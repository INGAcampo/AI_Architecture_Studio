import hashlib,json
from pathlib import Path
class ReissueExecutiveProject:
 required=('GEO-001','GEO-002','GEO-003','GEO-004','PROJ-001','PROJ-002','PROJ-003','DOC-001')
 def prepare(self,payload_path,output_path):
  p=Path(payload_path); data=json.loads(p.read_text()); v=data.get('values',{}); missing=[x for x in self.required if v.get(x) in (None,'')]
  if not data.get('provenance',{}).get('source_sha256'): missing.append('provenance.source_sha256')
  r={'command':'ReissueExecutiveProject','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'missing':missing,'pipeline':['Validate External Inputs','Update Graph','Selective Regeneration','QA/QC','Executive Manifest'],'verdict':'WAITING_FOR_AUTHENTICATED_EXTERNAL_PROJECT_INPUTS' if missing else 'READY_TO_RUN_REENTRY'}
  Path(output_path).write_text(json.dumps(r,indent=2)); return r
