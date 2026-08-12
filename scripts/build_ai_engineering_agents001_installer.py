from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; TARGET=ROOT/"AIAS_AI_ENGINEERING_AGENTS001_INSTALLER"
def main():
    if TARGET.exists(): shutil.rmtree(TARGET)
    payload=TARGET/"payload"
    for rel in ("src/aias_engineering_agents","engineering/aias/engineering_agents","docs/AI_ENGINEERING_AGENTS_001.md","tests/test_ai_engineering_agents001.py"):
        s,d=ROOT/rel,payload/rel; d.parent.mkdir(parents=True,exist_ok=True); shutil.copytree(s,d) if s.is_dir() else shutil.copy2(s,d)
    (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AI-ENGINEERING-AGENTS-001","version":"1.0.0","status":"CONTRACT_ACTIVATED","validation_first":True},indent=2)+"\n",encoding="utf-8")
    fs=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256"); (TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in fs)+"\n",encoding="utf-8"); print(json.dumps({"target":str(TARGET),"files":len(fs)}))
if __name__=="__main__": main()
