from pathlib import Path
import hashlib, shutil
r=Path(__file__).resolve().parents[1]; o=r/'AIAS_NEXT039_ARCHIVE_INSTALLER'
if o.exists(): shutil.rmtree(o)
o.mkdir(); fs=[r/'src/aias_next039_archive/__init__.py',r/'src/aias_next039_archive/archive.py',r/'engineering/aias/next039_archive/AIAS_NEXT_039_SPEC.json',r/'docs/AIAS_NEXT_039_ARCHIVE.md']
for s in fs:
 t=o/s.relative_to(r); t.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(s,t)
(o/'checksums.sha256').write_text('\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(o).as_posix()}' for p in sorted(o.rglob('*')) if p.is_file())+'\n')
