from pathlib import Path
import json
root = Path(__file__).resolve().parents[1]
out = root / "engineering" / "aias" / "installers" / "PP08_AUTOMATED_QA_QC_DESIGN_LOOP_V0_INSTALLER.json"
manifest = {"installer":"PP08_AUTOMATED_QA_QC_DESIGN_LOOP_V0_INSTALLER","files":["src/aias_qa_core/__init__.py","src/aias_qa_core/qa.py","tests/project_production/test_qa_core.py"],"status":"READY"}
out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps(manifest, indent=2))
