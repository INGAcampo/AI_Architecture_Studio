from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_I18N_CORE002_PRIORITY_GUI_LOCALIZATION_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for relative in ("src/aias_i18n","src/gui/project_session.py","src/gui/project_browser/qt_widget.py","src/gui/property_palette/model.py","src/gui/workspace/model.py","src/gui/workspace2/qt_command_palette.py","src/gui/workspace2/commanding.py","resources/i18n","engineering/aias/internationalization/I18N_CORE_002_SPEC.json","engineering/aias/internationalization/I18N_CORE_001_COVERAGE.json","engineering/i18n_core002/compliance","docs/I18N_CORE_002.md","tests/test_i18n_core002.py"):
  source,destination=ROOT/relative,PAYLOAD/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,destination,ignore=shutil.ignore_patterns("__pycache__","*.pyc")) if source.is_dir() else shutil.copy2(source,destination)
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"I18N-CORE-002","version":"1.0.0","status":"PRIORITY_SURFACES_LOCALIZED_REMAINING_GAPS","baseline_candidates":255,"current_candidates":218,"full_gui_translation_claimed":False,"next":"I18N-CORE-003"},indent=2)+"\n",encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(json.dumps({"target":str(TARGET),"files":len(files)}))
if __name__=="__main__":main()
