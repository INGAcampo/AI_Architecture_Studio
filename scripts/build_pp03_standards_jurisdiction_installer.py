from pathlib import Path
import hashlib, shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'installers'/'PP03_STANDARDS_JURISDICTION_V0_INSTALLER'
FILES=[ROOT/'src/aias_standards_core/__init__.py',ROOT/'src/aias_standards_core/engine.py',ROOT/'tests/project_production/test_standards_core.py',ROOT/'engineering/aias/project_production/PP-03_STANDARDS_JURISDICTION/STANDARDS_PACK_VE_PILOT_001.json',ROOT/'engineering/aias/project_production/PP-03_STANDARDS_JURISDICTION/PP03_V0.md']
OUT.mkdir(parents=True,exist_ok=True); lines=[]
for f in FILES:
 d=OUT/f.name; shutil.copy2(f,d); lines.append(f"{hashlib.sha256(d.read_bytes()).hexdigest()}  {d.name}")
(OUT/'SHA256SUMS').write_text('\n'.join(lines)+'\n',encoding='utf-8'); print('PP03_STANDARDS_JURISDICTION_V0_INSTALLER: 5 files checksummed')
