from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"AIAS_AEC000052_EXPERIENCE_ECOSYSTEM_INSTALLER"
PAYLOAD=TARGET/"payload"

def main():
    if TARGET.exists():shutil.rmtree(TARGET)
    copies=(
        "engineering/aeps/02_CONSTITUTION/AEC-000002-executable-constitution.yaml",
        "engineering/aias/master/AIAS_EXPERIENCE_AND_ECOSYSTEM_POLICY.json",
        "engineering/aias/master/AIAS_MASTER_DEVELOPMENT_PLAN.json",
        "tests/test_aec000052_experience_rule.py",
    )
    for relative in copies:
        source=ROOT/relative;target=PAYLOAD/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-AEC-000052","version":"1.0.0","status":"ACTIVE","surfaces":["desktop","installer","installation_iso","website","apps","social_channels","learning_channel","brand"],"historical_authority":"AIAS-GENESIS-CHAT01","false_completion_claims":False},indent=2)+"\n",encoding="utf-8")
    (TARGET/"README_INSTALACION.md").write_text("# AEC-000052 Experience and Ecosystem\n\nInstalls the permanent maximum-stewardship and exceptional-experience rule with truthful surface status.\n",encoding="utf-8")
    files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256")
    (TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8")
    print({"target":str(TARGET),"files":len(files)})

if __name__=="__main__":main()
