from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_ROADMAP_RECONCILIATION002_HISTORICAL_EVIDENCE_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for relative in ("src/aias_roadmap_audit/reconciliation.py","src/aias_roadmap_audit/__init__.py","engineering/aias/history/chat01/CHAT01_MATERIALIZATION_GAP.json","engineering/aias/history/chat01/CHAT01_DECISION_REGISTER.json","engineering/aias/roadmap/ROADMAP_RECONCILIATION_002.json","engineering/aias/roadmap/ROADMAP_RECONCILIATION_002_SPEC.json","engineering/roadmap_reconciliation002/compliance","docs/ROADMAP_RECONCILIATION_002.md","tests/test_roadmap_reconciliation002.py","scripts/build_roadmap_reconciliation002_report.py"):
  source,destination=ROOT/relative,PAYLOAD/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,destination,ignore=shutil.ignore_patterns("__pycache__","*.pyc")) if source.is_dir() else shutil.copy2(source,destination)
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"ROADMAP-RECONCILIATION-002","version":"1.0.0","status":"VALIDATED","next":"I18N-CORE-001"},indent=2)+"\n",encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(json.dumps({"target":str(TARGET),"files":len(files)}))
if __name__=="__main__":main()
