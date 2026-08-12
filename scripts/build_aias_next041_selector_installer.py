from pathlib import Path
import hashlib,shutil
r=Path(__file__).resolve().parents[1];o=r/'AIAS_NEXT041_SELECTOR_INSTALLER'
if o.exists():shutil.rmtree(o)
o.mkdir();fs=[r/'src/aias_next041_selector/__init__.py',r/'src/aias_next041_selector/selector.py',r/'engineering/aias/next041_selector/AIAS_NEXT_041_SPEC.json',r/'docs/AIAS_NEXT_041_SELECTOR.md']
for s in fs:
 t=o/s.relative_to(r);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s,t)
(o/'checksums.sha256').write_text('\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(o).as_posix()}' for p in sorted(o.rglob('*')) if p.is_file())+'\n')
