"""Public module supporting the sixth Omega integrated product release."""
import argparse,json
from pathlib import Path
from .workflow import build_and_export
def main():
    """Execute the public main operation for the sixth Omega integrated product release using explicit caller inputs."""
    p=argparse.ArgumentParser(); p.add_argument("command",choices=["doctor","demo"]); p.add_argument("--output",default="omega_release_6_outputs"); a=p.parse_args()
    if a.command=="doctor": print(json.dumps({"version":"6.0.0","cost_catalog":True,"boq":True,"csv":True,"json":True,"markdown":True},indent=2)); return 0
    project,lines,paths=build_and_export(Path(a.output).resolve())
    print("boq_lines:",len(lines)); print("total:",sum(x.total for x in lines))
    [print(k,":",v) for k,v in paths.items()]; return 0
if __name__=="__main__": raise SystemExit(main())
