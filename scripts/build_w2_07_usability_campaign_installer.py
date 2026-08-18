from pathlib import Path
import hashlib
import shutil

root = Path(__file__).resolve().parents[1]
out = root / "AIAS_W2_07_USABILITY_CAMPAIGN_INSTALLER"
if out.exists():
    shutil.rmtree(out)
out.mkdir()
files = [root / "src/aias_usability_campaign/__init__.py", root / "src/aias_usability_campaign/campaign.py", root / "engineering/aias/usability_campaign/AIAS_W2_07_SPEC.json", root / "engineering/aias/usability_campaign/SESSION_TEMPLATE.json", root / "docs/AIAS_W2_07_USABILITY_CAMPAIGN.md"]
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
