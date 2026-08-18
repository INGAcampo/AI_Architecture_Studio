"""Public module supporting the fifth Omega integrated product release."""
import argparse,json
from .workflow import solve_demo_truss
def main():
    """Execute the public main operation for the fifth Omega integrated product release using explicit caller inputs."""
    p=argparse.ArgumentParser(); p.add_argument("command",choices=["doctor","demo"]); a=p.parse_args()
    if a.command=="doctor": print(json.dumps({"version":"5.0.0","truss_2d_solver":True,"reactions":True,"axial_forces":True},indent=2)); return 0
    r=solve_demo_truss(); print(json.dumps({"displacements":r.displacements,"reactions":r.reactions,"axial_forces":r.axial_forces},indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
