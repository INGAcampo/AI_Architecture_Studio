from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"AIAS_DESIGN_SYSTEM001_EXPERIENCE_FOUNDATION_INSTALLER"
PAYLOAD=TARGET/"payload"

def main():
    if TARGET.exists():shutil.rmtree(TARGET)
    shutil.copytree(ROOT/"src/aias_design_system",PAYLOAD/"src/aias_design_system",ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
    copies=("engineering/aias/experience/AIAS_DESIGN_SYSTEM_SPEC.json","engineering/aias/experience/AIAS_CURRENT_UI_MIGRATION_BASELINE.json","docs/AIAS_DESIGN_SYSTEM_001.md","tests/test_aias_design_system001.py")
    for relative in copies:
        source=ROOT/relative;target=PAYLOAD/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    manifest={"pack_id":"AIAS-DESIGN-SYSTEM-001","version":"0.1.0","status":"FOUNDATION_IMPLEMENTED_RENDERED_APPROVAL_PENDING","governing_article":"AEC-000052","themes":["dark","light"],"consumers":["desktop","installer","installation_iso","website","apps","documents","learning"],"legacy_ui_migrated":False,"next":"AIAS-UX-AUDIT-001"}
    (TARGET/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    (TARGET/"README_INSTALACION.md").write_text("# AIAS Design System 001\n\nInstalls semantic tokens, generated Qt themes, UI migration audit and cross-surface experience specification. Visual freeze requires rendered Project Director approval.\n",encoding="utf-8")
    files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256")
    (TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8")
    print({"target":str(TARGET),"files":len(files)})

if __name__=="__main__":main()
