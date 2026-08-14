from pathlib import Path
import hashlib, shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'installers'/'PP05_DOCUMENTATION_DRAWING_PRODUCTION_V0_INSTALLER'
FILES=[ROOT/'src/aias_drawing_core/__init__.py',ROOT/'src/aias_drawing_core/drawing.py',ROOT/'tests/project_production/test_drawing_core.py',ROOT/'engineering/aias/project_production/PP-05_DOCUMENTATION_DRAWING_PRODUCTION/PP05_SPEC.json',ROOT/'engineering/aias/project_production/PP-05_DOCUMENTATION_DRAWING_PRODUCTION/PP05_V0.md']
OUT.mkdir(parents=True,exist_ok=True); lines=[]
for f in FILES:
 d=OUT/f.name; shutil.copy2(f,d); lines.append(f"{hashlib.sha256(d.read_bytes()).hexdigest()}  {d.name}")
(OUT/'SHA256SUMS').write_text('\n'.join(lines)+'\n',encoding='utf-8'); print('PP05_DOCUMENTATION_DRAWING_PRODUCTION_V0_INSTALLER: 5 files checksummed')
