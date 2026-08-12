from pathlib import Path
import hashlib,shutil
r=Path(__file__).resolve().parents[1];o=r/'AIAS_NEXT068_INTEGRITY_INSTALLER'
if o.exists():shutil.rmtree(o)
o.mkdir();fs=[r/'src/aias_next068_integrity/__init__.py',r/'src/aias_next068_integrity/report.py',r/'engineering/aias/next068_integrity/AIAS_NEXT_068_SPEC.json',r'docs/AIAS_NEXT_068_INTEGRITY.md']
fs[-1]=r/'docs/AIAS_NEXT_068_INTEGRITY.md'
for s in fs:
 t=o/s.relative_to(r);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s,t)
(o/'checksums.sha256').write_text('\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(o).as_posix()}' for p in sorted(o.rglob('*')) if p.is_file())+'\n')
