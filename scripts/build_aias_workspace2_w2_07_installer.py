from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_WORKSPACE2_W2_07_VALIDATION_CAMPAIGN_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for relative in ("src/gui/workspace2/experience_validation.py","engineering/aias/experience/AIAS_WORKSPACE2_W2_07_SPEC.json","engineering/aias/experience/AIAS_WORKSPACE2_W2_07_USABILITY_PROTOCOL.json","docs/AIAS_WORKSPACE2_W2_07.md","tests/test_aias_workspace2_w2_07.py","workspace2_w2_07_outputs/AUTOMATED_VALIDATION_REPORT.json","workspace2_w2_07_outputs/REPRESENTATIVE_SESSION_LEDGER.json"):
  source,destination=ROOT/relative,PAYLOAD/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,destination)
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-WORKSPACE-2.0-W2-07","version":"0.7.0","status":"AUTOMATED_VALIDATION_PASSED_REPRESENTATIVE_SESSIONS_PENDING","next_parallel":"EXP-INSTALLER-ISO-001"},indent=2)+"\n",encoding="utf-8");files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(json.dumps({"target":str(TARGET),"files":len(files)}))
if __name__=="__main__":main()
