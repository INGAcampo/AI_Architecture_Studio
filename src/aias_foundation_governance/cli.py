"""CLI for validating and releasing AIAS institutional foundations."""
import argparse,json
from pathlib import Path
from .orchestrator import FoundationGovernanceOrchestrator
def main():
 """Validate Charter and Handbook from a repository root."""
 p=argparse.ArgumentParser();p.add_argument("--project-root",default=".");p.add_argument("--output",default="foundation_align001_outputs");a=p.parse_args();print(json.dumps(FoundationGovernanceOrchestrator().execute(Path(a.project_root).resolve(),Path(a.output).resolve()),indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
