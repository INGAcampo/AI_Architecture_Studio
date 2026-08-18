from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"AIAS_GENESIS_CHAT01_FOUNDATIONAL_RECORD_INSTALLER"
PAYLOAD=TARGET/"payload"

def main():
    if TARGET.exists():shutil.rmtree(TARGET)
    (PAYLOAD/"engineering/aias/history/chat01").mkdir(parents=True)
    (PAYLOAD/"tests").mkdir(parents=True)
    for source in sorted((ROOT/"engineering/aias/history/chat01").iterdir()):
        if source.is_file():shutil.copy2(source,PAYLOAD/"engineering/aias/history/chat01"/source.name)
    shutil.copy2(ROOT/"tests/test_chat01_genesis_record.py",PAYLOAD/"tests")
    manifest={"pack_id":"AIAS-GENESIS-CHAT01","version":"1.0.0","status":"FOUNDATIONAL_HISTORY_MATERIALIZED","source_images":155,"decisions":20,"authority_boundary":"Historical assistant claims require current repository evidence","outputs":["SOURCE_MANIFEST","GENESIS_NARRATIVE","DECISION_REGISTER","MATERIALIZATION_GAP"]}
    (TARGET/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    (TARGET/"README_INSTALACION.md").write_text("# AIAS Genesis Chat 01\n\nInstalls the verified foundational-history record without copying screenshot images or treating historical package claims as current evidence.\n",encoding="utf-8")
    files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256")
    (TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8")
    print({"target":str(TARGET),"files":len(files)})

if __name__=="__main__":main()
