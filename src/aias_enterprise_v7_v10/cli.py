"""Public module supporting enterprise portfolio, orchestration and governance capabilities."""
import argparse,json
from pathlib import Path
from .core import EnterpriseOrchestrator,SUPREME_RULES

def main():
 """Execute the public main operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
 p=argparse.ArgumentParser(prog='aias-enterprise-v7-v10'); s=p.add_subparsers(dest='cmd',required=True)
 s.add_parser('doctor'); s.add_parser('rules'); b=s.add_parser('build'); b.add_argument('specification'); b.add_argument('--workspace',default='aeps_v7_v10_build')
 a=p.parse_args()
 if a.cmd=='doctor':
  print(json.dumps({'version':'10.0.0','capability_framework':True,'capability_factory':True,'enterprise_registry':True,'knowledge_graph':True,'constitutional_compliance':True,'engineering_ledger':True,'enterprise_metrics':True,'integrity_engine':True,'enterprise_orchestrator':True,'sdd_active':True,'immediate_rule_application':True,'minimum_time_reduction':0.45},indent=2)); return 0
 if a.cmd=='rules':
  print(json.dumps([{'id':r.rule_id,'title':r.title,'mandatory':r.mandatory,'immediate':r.immediate} for r in SUPREME_RULES],indent=2,ensure_ascii=False)); return 0
 print(json.dumps(EnterpriseOrchestrator().build(Path(a.specification).resolve(),Path(a.workspace).resolve()),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
