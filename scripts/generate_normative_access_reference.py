from __future__ import annotations
import json
from pathlib import Path
from aias_normative_access import certification_scope, normative_assets
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"engineering/aias/certification"
def main():
 OUT.mkdir(parents=True,exist_ok=True);(OUT/"NORMATIVE_ACCESS_REGISTRY.json").write_text(json.dumps({"status":"ACQUISITION_NOT_AUTHORIZED","assets":normative_assets()},indent=2)+"\n",encoding="utf-8");(OUT/"CERTIFICATION_SCOPE.json").write_text(json.dumps(certification_scope(),indent=2)+"\n",encoding="utf-8");print({"assets":len(normative_assets()),"purchases":0,"providers_selected":0})
if __name__=="__main__":main()
