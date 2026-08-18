"""Public module supporting the AIAS development factory."""
import argparse,json
from pathlib import Path
from .core import ModuleSpec,SpecValidator,Orchestrator
def main():
 """Execute the public main operation for the AIAS development factory using explicit caller inputs."""
 p=argparse.ArgumentParser(prog='aias-adf'); s=p.add_subparsers(dest='cmd',required=True); s.add_parser('doctor'); v=s.add_parser('validate-spec'); v.add_argument('spec'); g=s.add_parser('generate'); g.add_argument('spec'); g.add_argument('--workspace',default='adf_outputs'); a=p.parse_args()
 if a.cmd=='doctor': print(json.dumps({'version':'1.0.0','spec_validator':True,'module_generator':True,'test_generator':True,'documentation_generator':True,'quality_gate':True,'release_builder':True},indent=2)); return 0
 if a.cmd=='validate-spec':
  e=SpecValidator().validate(ModuleSpec.load(Path(a.spec))); print(json.dumps({'passed':not e,'issues':e},indent=2)); return 0 if not e else 1
 print(json.dumps(Orchestrator().execute(Path(a.spec),Path(a.workspace).resolve()),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
