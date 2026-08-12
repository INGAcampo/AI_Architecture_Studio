from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_CERTIFICATION_NORMATIVE_ACCESS001_PROCUREMENT_READINESS_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 (PAYLOAD/"src").mkdir(parents=True);(PAYLOAD/"tests").mkdir();(PAYLOAD/"docs").mkdir();(PAYLOAD/"engineering/aias/certification").mkdir(parents=True)
 shutil.copytree(ROOT/"src/aias_normative_access",PAYLOAD/"src/aias_normative_access",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests/test_certification_normative_access001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/CERTIFICATION_NORMATIVE_ACCESS001.md",PAYLOAD/"docs")
 for name in ("NORMATIVE_ACCESS_PLAN.json","EXTERNAL_GAP_ASSESSMENT_RFP.json","NORMATIVE_ACCESS_REGISTRY.json","CERTIFICATION_SCOPE.json"):shutil.copy2(ROOT/"engineering/aias/certification"/name,PAYLOAD/"engineering/aias/certification")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-CERTIFICATION-NORMATIVE-ACCESS-001","version":"1.0.0","status":"PROCUREMENT_READY_NOT_AUTHORIZED","purchases_executed":False,"providers_selected":False,"certification_claim":False},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# CERTIFICATION-NORMATIVE-ACCESS-001 Installer\n\nPreparation only; no purchase, outreach or contract is authorized.\n",encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
if __name__=="__main__":main()
