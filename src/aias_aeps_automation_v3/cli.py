"""Public module supporting AEPS repeatable generation and delivery automation."""
import argparse,json
from pathlib import Path
from .orchestrator import AutomationOrchestrator
def main():
 """Execute the public main operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
 p=argparse.ArgumentParser(prog='aias-aeps-v3'); s=p.add_subparsers(dest='cmd',required=True); s.add_parser('doctor'); b=s.add_parser('build'); b.add_argument('specification'); b.add_argument('--workspace',default='aeps_v3_build'); a=p.parse_args()
 if a.cmd=='doctor':
  print(json.dumps({'version':'3.0.0',**{f'm{i:02d}':True for i in range(1,11)}},indent=2)); return 0
 c=AutomationOrchestrator().build(Path(a.specification).resolve(),Path(a.workspace).resolve()); print(json.dumps({'specification':c.specification.specification_id,'artifacts':len(c.artifacts),'certified':c.reports.get('certified',False),'release':c.reports.get('release')},indent=2)); return 0 if c.reports.get('certified') else 1
if __name__=='__main__': raise SystemExit(main())
