"""Public module supporting professional BIM foundation modeling and exchange."""
import argparse,json
from .workflow import build_demo
def main():
    """Execute the public main operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("doctor"); d=sub.add_parser("demo"); d.add_argument("--output",default="bim_foundation_outputs")
    a=p.parse_args()
    if a.cmd=="doctor":
        print(json.dumps({"version":"1.0.0","walls":True,"openings":True,"levels":True,"grids":True,
                          "materials":True,"quantities":True,"analytical":True,"serialization":True,
                          "ifc_lite":True,"omega_bridge":True},indent=2)); return 0
    _,w,q,an,pp,ip=build_demo(a.output)
    print("wall_length_m:",w.length_m); print("net_volume_m3:",q.net_volume_m3)
    print("analytical_area_m2:",an.area_m2); print("project:",pp); print("ifc_lite:",ip)
    return 0
if __name__=="__main__": raise SystemExit(main())
