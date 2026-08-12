from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "AIAS_FOUNDATION_ALIGN001_CHARTER_HANDBOOK_INSTALLER"
PAYLOAD = TARGET / "payload"

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    if TARGET.exists():
        shutil.rmtree(TARGET)
    for folder in ("src", "tests", "docs", "engineering/aias/foundation"):
        (PAYLOAD / folder).mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "src" / "aias_foundation_governance", PAYLOAD / "src" / "aias_foundation_governance", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(ROOT / "tests" / "test_foundation_align001.py", PAYLOAD / "tests")
    shutil.copy2(ROOT / "docs" / "FOUNDATION_ALIGN001_CHARTER_HANDBOOK.md", PAYLOAD / "docs")
    for name in ("AIAS_CHARTER.json", "AIAS_ARCHITECTURE_HANDBOOK.json"):
        shutil.copy2(ROOT / "engineering" / "aias" / "foundation" / name, PAYLOAD / "engineering" / "aias" / "foundation")
    manifest = {"pack_id":"AIAS-FOUNDATION-ALIGN-001","version":"1.0.0","outputs":["CANONICAL_CHARTER","EXECUTABLE_ARCHITECTURE_HANDBOOK","HIERARCHY_VALIDATOR","REPRODUCIBLE_RELEASE"],"legal_status":"GOVERNANCE_CONTROL"}
    (TARGET / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (TARGET / "README_INSTALACION.md").write_text("# FOUNDATION-ALIGN-001 Installer\n\nInstala y valida el Charter y el Architecture Handbook ejecutables de AIAS.\n", encoding="utf-8")
    (TARGET / "install_foundation_align001.py").write_text(INSTALLER, encoding="utf-8")
    files = sorted(path for path in TARGET.rglob("*") if path.is_file() and path.name != "checksums.sha256")
    (TARGET / "checksums.sha256").write_text("\n".join(f"{digest(path)}  {path.relative_to(TARGET).as_posix()}" for path in files) + "\n", encoding="utf-8")
    print(TARGET)

INSTALLER = r'''import argparse, shutil, subprocess, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
shutil.copytree(h/"payload"/"src"/"aias_foundation_governance",r/"src"/"aias_foundation_governance",dirs_exist_ok=True)
shutil.copytree(h/"payload"/"engineering"/"aias"/"foundation",r/"engineering"/"aias"/"foundation",dirs_exist_ok=True)
shutil.copy2(h/"payload"/"tests"/"test_foundation_align001.py",r/"tests")
raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_foundation_align001.py"),"-q"],cwd=r).returncode)
'''

if __name__ == "__main__":
    main()
