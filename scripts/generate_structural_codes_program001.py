from pathlib import Path
import json
from aias_structural_codes_program import knowledge_baseline,program_roadmap,validate_program
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"engineering/aias/structural_codes"
def main():
 OUT.mkdir(parents=True,exist_ok=True);roadmap=program_roadmap();issues=validate_program(roadmap)
 (OUT/"STRUCTURAL_PLATFORM_ROADMAP.json").write_text(json.dumps(roadmap,indent=2)+"\n",encoding="utf-8")
 (OUT/"LIVING_KNOWLEDGE_BASELINE.json").write_text(json.dumps(knowledge_baseline(ROOT),indent=2)+"\n",encoding="utf-8")
 print({"program":roadmap["program_id"],"stages":len(roadmap["stages"]),"issues":issues});raise SystemExit(bool(issues))
if __name__=="__main__":main()
