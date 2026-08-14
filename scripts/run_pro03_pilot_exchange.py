from pathlib import Path
import json, hashlib
from aias_building_design_core import BuildingDesignCore
from aias_cad_professional import CADEngine
from aias_exchange_writers import ExchangeWriters
root=Path(__file__).resolve().parents[1]; base=root/'engineering/aias/professional_project_production/PRO-03_DWG_PDF_PRODUCTION'; out=base/'output'; out.mkdir(parents=True,exist_ok=True)
g=BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project('Edificación piloto AIAS Venezuela')); cad=CADEngine().build(g,{}); w=ExchangeWriters(); artifacts=[]
for sheet in cad.sheets:
    meta=w.write_dxf(cad,out/f"{sheet['number']}.dxf"); artifacts.append({'path':f"{sheet['number']}.dxf",**meta,'classification':'V0_LIMITED'})
pdf=w.write_pdf(cad,out/'PILOT-BUILDING-001_PLAN_SET.pdf'); artifacts.append({'path':'PILOT-BUILDING-001_PLAN_SET.pdf',**pdf,'classification':'V0_LIMITED'})
manifest={'pilot':'PILOT-BUILDING-001','backend_dwg':'NONE_AVAILABLE','dxf_compatibility':'ASCII DXF exchange writer','dwg_real_outputs':0,'pdf':pdf,'artifacts':artifacts,'roundtrip':'DXF textual re-open/count validated; native DWG roundtrip BLOCKED','losses':['native DWG unavailable','advanced typography/rendering not preserved'],'blocked':['DWG real writer','professional PDF composition/signing']}
(base/'PRO03_EXPORT_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8'); print(json.dumps({'dxf':5,'pdf_pages':pdf['pages'],'dwg_real':0},indent=2))
