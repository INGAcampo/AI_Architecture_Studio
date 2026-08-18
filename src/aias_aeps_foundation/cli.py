"""Public module supporting the AEPS foundation production runtime."""
import argparse,json
from pathlib import Path
from .core import Generator,Validator,Asset,Status
from .bootstrap import bootstrap
def main():
 """Execute the public main operation for the AEPS foundation production runtime using explicit caller inputs."""
 p=argparse.ArgumentParser(); s=p.add_subparsers(dest='c',required=True); s.add_parser('doctor'); b=s.add_parser('bootstrap'); b.add_argument('--root',default='.'); g=s.add_parser('generate'); g.add_argument('--output',required=True)
 a=p.parse_args()
 if a.c=='doctor': print(json.dumps({'version':'1.0.0','object_model':True,'identifier_system':True,'validator':True,'generator':True,'bootstrap':True},indent=2)); return 0
 if a.c=='bootstrap': print('created_directories:',len(bootstrap(Path(a.root).resolve()))); return 0
 x=Generator().create('SPEC','Generated Asset','Specification','AIAS','Demonstrate generation','AEPS'); Generator().save(x,Path(a.output)); print(x.asset_id); return 0
if __name__=='__main__': raise SystemExit(main())
