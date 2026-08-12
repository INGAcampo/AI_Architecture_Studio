from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "AIAS_ECP000001D_FOUNDATION_DETAILING_DOCUMENTATION_INSTALLER"
PAYLOAD = TARGET / "payload"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if TARGET.exists():
        shutil.rmtree(TARGET)
    (PAYLOAD / "src").mkdir(parents=True)
    (PAYLOAD / "tests").mkdir()
    (PAYLOAD / "docs").mkdir()
    shutil.copytree(
        ROOT / "src" / "aias_foundation_documentation",
        PAYLOAD / "src" / "aias_foundation_documentation",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )
    shutil.copy2(ROOT / "tests" / "test_ecp000001d_foundation_documentation.py", PAYLOAD / "tests")
    shutil.copy2(ROOT / "docs" / "ECP000001D_FOUNDATION_DETAILING_DOCUMENTATION.md", PAYLOAD / "docs")
    manifest = {
        "pack_id": "AIAS-ECP-000001D-FOUNDATION-DETAILING-DOCUMENTATION",
        "version": "1.0.0",
        "expected_focused_tests": 10,
        "consumes": ["ECP-000001A", "ECP-000001B", "ECP-000001C"],
        "outputs": ["SVG_PLAN", "SVG_SECTION", "BAR_SCHEDULE_CSV", "QUANTITIES", "TECHNICAL_JSON", "TECHNICAL_REPORT", "RELEASE_ZIP"],
        "legal_status": "REFERENCE_ONLY",
        "human_review_required": True,
    }
    (TARGET / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (TARGET / "README_INSTALACION.md").write_text(
        "# ECP-000001D Installer\n\n"
        "```powershell\ncd \"C:\\AIAS\\AI_Architecture_Studio\\AIAS_ECP000001D_FOUNDATION_DETAILING_DOCUMENTATION_INSTALLER\"\n"
        "& \"..\\.venv\\Scripts\\python.exe\" \".\\install_ecp000001d.py\" --project-root \"C:\\AIAS\\AI_Architecture_Studio\"\n```\n",
        encoding="utf-8",
    )
    (TARGET / "install_ecp000001d.py").write_text(INSTALLER, encoding="utf-8")
    (TARGET / "run_ecp000001d.py").write_text(RUNNER, encoding="utf-8")
    files = sorted(path for path in TARGET.rglob("*") if path.is_file() and path.name != "checksums.sha256")
    (TARGET / "checksums.sha256").write_text("\n".join(f"{digest(path)}  {path.relative_to(TARGET).as_posix()}" for path in files) + "\n", encoding="utf-8")
    print(TARGET)


INSTALLER = r'''from __future__ import annotations
import argparse, shutil, subprocess, sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--project-root",required=True); args=parser.parse_args()
    here=Path(__file__).resolve().parent; root=Path(args.project_root).resolve(); payload=here/"payload"
    shutil.copytree(payload/"src"/"aias_foundation_documentation",root/"src"/"aias_foundation_documentation",dirs_exist_ok=True)
    shutil.copy2(payload/"tests"/"test_ecp000001d_foundation_documentation.py",root/"tests")
    shutil.copy2(payload/"docs"/"ECP000001D_FOUNDATION_DETAILING_DOCUMENTATION.md",root/"docs")
    result=subprocess.run([sys.executable,"-m","pytest",str(root/"tests"/"test_ecp000001d_foundation_documentation.py"),"-q"],cwd=root)
    return result.returncode
if __name__=="__main__": raise SystemExit(main())
'''

RUNNER = r'''from pathlib import Path
from aias_foundation_documentation.orchestrator import FoundationDocumentationOrchestrator
if __name__=="__main__": print(FoundationDocumentationOrchestrator().execute(Path("ecp000001d_outputs").resolve()))
'''


if __name__ == "__main__":
    main()
