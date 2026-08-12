from pathlib import Path
import hashlib
import shutil

root = Path(__file__).resolve().parents[1]
out = root / "AIAS_NEXT018_HUMAN_REVIEW_HANDOFF_INSTALLER"
if out.exists():
    shutil.rmtree(out)
out.mkdir()
files = [root / "src/aias_next018_handoff/__init__.py", root / "src/aias_next018_handoff/handoff.py", root / "engineering/aias/next018_handoff/AIAS_NEXT_018_SPEC.json", root / "docs/AIAS_NEXT_018_HANDOFF.md"]
for source in files:
    target = out / source.relative_to(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(out).as_posix()}" for path in sorted(out.rglob("*")) if path.is_file()]
(out / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(out)
