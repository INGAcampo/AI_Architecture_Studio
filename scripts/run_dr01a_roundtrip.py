from pathlib import Path
import json
from aias_autocad_backend import run_roundtrip
root=Path(__file__).resolve().parents[1]; source=root/'engineering/aias/professional_project_production/PRO-03_DWG_PDF_PRODUCTION/output'; out=root/'engineering/aias/dependency_resolution/DR-01A_NATIVE_DWG_ROUNDTRIP/output'
result=run_roundtrip(source,out); (out.parent/'DR01A_DWG_ROUNDTRIP_MANIFEST.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps({'verdict':result['verdict'],'drawings':len(result.get('drawings',[]))},indent=2))
