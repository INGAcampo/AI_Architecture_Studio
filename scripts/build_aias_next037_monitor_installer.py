from pathlib import Path
import hashlib, shutil
root=Path(__file__).resolve().parents[1]; out=root/'AIAS_NEXT037_MONITOR_INSTALLER'
if out.exists(): shutil.rmtree(out)
out.mkdir()
files=[root/'src/aias_next037_monitor/__init__.py',root/'src/aias_next037_monitor/cycle.py',root/'engineering/aias/next037_monitor/AIAS_NEXT_037_SPEC.json',root/'docs/AIAS_NEXT_037_MONITOR.md']
for s in files:
 t=out/s.relative_to(root); t.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(s,t)
(out/'checksums.sha256').write_text('\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(out).as_posix()}' for p in sorted(out.rglob('*')) if p.is_file())+'\n',encoding='utf-8')
print(out)
