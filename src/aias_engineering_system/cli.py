"""Public module supporting the executable AIAS engineering operating system."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .validator import EngineeringSystemValidator
def main()->int:
 """Execute the public main operation for the executable AIAS engineering operating system using explicit caller inputs."""
 p=argparse.ArgumentParser();p.add_argument("--project-root",default=".");a=p.parse_args();root=Path(a.project_root).resolve();base=root/"engineering"/"aias"/"foundation";result=EngineeringSystemValidator().validate(base/"AIAS_ENGINEERING_SYSTEM.json",base/"AIAS_AES_STANDARDS_REGISTRY.json");print(json.dumps(result,indent=2));return 0 if result["valid"] else 1
if __name__=="__main__":raise SystemExit(main())
