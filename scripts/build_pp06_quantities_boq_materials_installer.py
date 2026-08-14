from pathlib import Path
import hashlib, shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'installers'/'PP06_QUANTITIES_BOQ_MATERIALS_V0_INSTALLER'
FILES=[ROOT/'src/aias_quantities_core/__init__.py',ROOT/'src/aias_quantities_core/quantities.py',ROOT/'tests/project_production/test_quantities_core.py',ROOT/'engineering/aias/project_production/PP-06_QUANTITIES_BOQ_MATERIALS/PP06_SPEC.json',ROOT/'engineering/aias/project_production/PP-06_QUANTITIES_BOQ_MATERIALS/PP06_V0.md']
OUT.mkdir(parents=True,exist_ok=True); lines=[]
for f in FILES:
 d=OUT/f.name; shutil.copy2(f,d); lines.append(f"{hashlib.sha256(d.read_bytes()).hexdigest()}  {d.name}")
(OUT/'SHA256SUMS').write_text('\n'.join(lines)+'\n',encoding='utf-8'); print('PP06_QUANTITIES_BOQ_MATERIALS_V0_INSTALLER: 5 files checksummed')
