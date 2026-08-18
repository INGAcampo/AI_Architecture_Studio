from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "engineering" / "aias" / "installers" / "PP07_MEMORIES_SPECIFICATIONS_REPORTS_V0_INSTALLER.json"
manifest = {"installer":"PP07_MEMORIES_SPECIFICATIONS_REPORTS_V0_INSTALLER","files":["src/aias_reports_core/__init__.py","src/aias_reports_core/reports.py","tests/project_production/test_reports_core.py"],"status":"READY"}
OUT.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps(manifest, indent=2))
