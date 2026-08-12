from pathlib import Path
import hashlib
import shutil

root = Path(__file__).resolve().parents[1]
out = root / "AIAS_NEXT012_EVIDENCE_BACKED_SELECTION_INSTALLER"
if out.exists():
    shutil.rmtree(out)
out.mkdir()
files = [root / "src/aias_next012_selection/__init__.py", root / "src/aias_next012_selection/selector.py", root / "engineering/aias/next012_selection/AIAS_NEXT_012_SPEC.json", root / "docs/AIAS_NEXT_012_SELECTION.md"]
for source in files:
    target = out / source.relative_to(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
lines = []
for path in sorted(out.rglob("*")):
    if path.is_file() and path.name != "checksums.sha256":
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(out).as_posix()}")
(out / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(out)
