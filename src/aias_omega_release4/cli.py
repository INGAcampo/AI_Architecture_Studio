"""Public module supporting the fourth Omega integrated product release."""
import argparse,json
from .workflow import build_bim_building
def main():
    """Execute the public main operation for the fourth Omega integrated product release using explicit caller inputs."""
    p=argparse.ArgumentParser(); p.add_argument("command",choices=["doctor","demo"]); a=p.parse_args()
    if a.command=="doctor":
        print(json.dumps({"version":"4.0.0","levels":True,"walls":True,"slabs":True,"doors":True,"windows":True,"net_quantities":True},indent=2)); return 0
    project,info=build_bim_building()
    print("objects:",len(project.objects)); print("relationships:",len(project.graph.all())); print("net_wall_volume_m3:",round(info["net_wall_volume_m3"],3)); return 0
if __name__=="__main__": raise SystemExit(main())
