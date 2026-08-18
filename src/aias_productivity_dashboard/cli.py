"""CLI for generating the permanent AIAS Productivity Dashboard."""
import argparse,json
from pathlib import Path
from .orchestrator import ProductivityDashboardOrchestrator
def main():
 """Generate a dashboard from an AIAS repository root."""
 p=argparse.ArgumentParser();p.add_argument("--project-root",default=".");p.add_argument("--output",default="aias_productivity_dashboard_outputs");a=p.parse_args();r=ProductivityDashboardOrchestrator().execute(Path(a.project_root).resolve(),Path(a.output).resolve());print(json.dumps(r,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
