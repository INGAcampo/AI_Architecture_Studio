from pathlib import Path
import hashlib
import shutil

root = Path(__file__).resolve().parents[1]
out = root / "AIAS_NEXT035_GOVERNANCE_CHECKPOINT_INSTALLER"
if out.exists():
    shutil.rmtree(out)
out.mkdir()
files = [root / "src/aias_next035_checkpoint/__init__.py", root / "src/aias_next035_checkpoint/checkpoint.py", root / "engineering/aias/next035_checkpoint/AIAS_NEXT_035_SPEC.json", root / "docs/AIAS_NEXT_035_CHECKPOINT.md"]
for source in files:
    target = out / source.relative_to(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(out).as_posix()}" for path in sorted(out.rglob("*")) if path.is_file()]
(out / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(out)
