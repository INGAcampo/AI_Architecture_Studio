from pathlib import Path
import json
from aias_cad_professional.engine import CADDocument
from aias_dxf_writer import ValidDxfWriter
from aias_autocad_backend import run_roundtrip
root=Path(__file__).resolve().parents[1]; base=root/'engineering/aias/dependency_resolution/DR-01A_R1_VALID_DXF_WRITER'; source=base/'output/source'; source.mkdir(parents=True,exist_ok=True)
model=json.loads((root/'engineering/aias/professional_project_production/PRO-02_PROFESSIONAL_CAD_DRAWING_ENGINE/PILOT-BUILDING-001_CAD_V0.json').read_text(encoding='utf-8')); cad=CADDocument(**model); mapping=ValidDxfWriter().write(cad,source/'A-101.dxf'); result=run_roundtrip(source,base/'output/roundtrip'); result['mapping']=mapping; result['format']='DXF R12 ASCII (AC1009)'; (base/'DR01AR1_MINIMUM_MANIFEST.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps({'verdict':result['verdict'],'mapping':len(mapping)},indent=2))
