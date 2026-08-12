from pathlib import Path
import hashlib,shutil
r=Path(__file__).resolve().parents[1];o=r/'AIAS_NEXT055_GOVERNANCE_INSTALLER'
if o.exists():shutil.rmtree(o)
o.mkdir();fs=[r/'src/aias_next055_governance/__init__.py',r/'src/aias_next055_governance/governance.py',r/'engineering/aias/next055_governance/AIAS_NEXT_055_SPEC.json',r/'docs/AIAS_NEXT_055_GOVERNANCE.md']
for s in fs:
 t=o/s.relative_to(r);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s,t)
(o/'checksums.sha256').write_text('\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(o).as_posix()}' for p in sorted(o.rglob('*')) if p.is_file())+'\n')
