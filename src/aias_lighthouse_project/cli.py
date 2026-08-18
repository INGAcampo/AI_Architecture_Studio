"""CLI for Project Lighthouse 001 generation."""
import argparse,json
from pathlib import Path
from .orchestrator import LighthouseOrchestrator
def main():
 """Generate the minimum reference-building slice."""
 p=argparse.ArgumentParser();p.add_argument("--workspace",default="lighthouse000001_outputs");a=p.parse_args();print(json.dumps(LighthouseOrchestrator().execute(Path(a.workspace).resolve()),indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
