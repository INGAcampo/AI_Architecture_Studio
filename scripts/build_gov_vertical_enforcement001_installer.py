from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_GOV_VERTICAL_ENFORCEMENT001_COMPLETE_DELIVERY_GATE_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for relative in ("src/aias_capability_factory/vertical.py","src/aias_capability_factory/factory.py","src/aias_capability_factory/__init__.py","engineering/aias/capability_factory/CAPABILITY_FACTORY_POLICY.json","engineering/aias/governance/GOV_VERTICAL_ENFORCEMENT_001_SPEC.json","engineering/gov_vertical_enforcement001/compliance","docs/GOV_VERTICAL_ENFORCEMENT_001.md","tests/test_gov_vertical_enforcement001.py","tests/test_capability_factory001.py"):
  source,destination=ROOT/relative,PAYLOAD/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,destination,ignore=shutil.ignore_patterns("__pycache__","*.pyc")) if source.is_dir() else shutil.copy2(source,destination)
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"GOV-VERTICAL-ENFORCEMENT-001","version":"1.0.0","status":"VALIDATED_FACTORY_ENFORCEMENT","retroactive_legacy_assessment_claimed":False,"next":"ROADMAP-RECONCILIATION-002"},indent=2)+"\n",encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(json.dumps({"target":str(TARGET),"files":len(files)}))
if __name__=="__main__":main()
