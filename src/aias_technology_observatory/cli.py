"""Command-line release entry point for the AIAS Technology Observatory."""
import argparse,json
from pathlib import Path
from .orchestrator import TechnologyObservatoryOrchestrator
def main():
 """Build and print an ATO opportunity portfolio release."""
 p=argparse.ArgumentParser();p.add_argument("--workspace",default="ecp000001g_outputs");a=p.parse_args();r=TechnologyObservatoryOrchestrator().execute(Path(a.workspace).resolve());print(json.dumps(r,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
