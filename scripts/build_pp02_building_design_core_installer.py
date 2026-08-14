from pathlib import Path
import hashlib, shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "installers" / "PP02_BUILDING_DESIGN_CORE_V0_INSTALLER"
FILES = [ROOT / "src/aias_building_design_core/__init__.py", ROOT / "src/aias_building_design_core/core.py", ROOT / "tests/project_production/test_building_design_core.py", ROOT / "engineering/aias/project_production/PP-02_BUILDING_DESIGN_CORE/PP02_SPEC.json", ROOT / "engineering/aias/project_production/PP-02_BUILDING_DESIGN_CORE/PP02_V0.md"]
OUT.mkdir(parents=True, exist_ok=True)
lines = []
for source in FILES:
    destination = OUT / source.name
    shutil.copy2(source, destination)
    lines.append(f"{hashlib.sha256(destination.read_bytes()).hexdigest()}  {destination.name}")
(OUT / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("PP02_BUILDING_DESIGN_CORE_V0_INSTALLER: 5 files checksummed")
