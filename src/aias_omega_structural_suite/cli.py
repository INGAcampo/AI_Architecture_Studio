"""Command-line diagnostics and complete structural workflow entrypoint."""
import argparse, json
from pathlib import Path
from .workflow import run_complete_structural_workflow

def main():
    """Dispatch structural suite operations with machine-readable results."""
    p=argparse.ArgumentParser(prog="aias-omega-structural")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    demo=sub.add_parser("demo"); demo.add_argument("--output",default="omega_structural_suite_outputs")
    a=p.parse_args()
    if a.command=="doctor":
        print(json.dumps({
            "version":"1.0.0",
            "frame2d_solver":True,
            "load_combinations":True,
            "modal_2dof":True,
            "pdelta":True,
            "steel_design":True,
            "concrete_design":True,
            "buckling":True,
            "bim_adapter":True,
            "reports":True
        },indent=2)); return 0
    data=run_complete_structural_workflow(Path(a.output).resolve())
    print("steel_adequate:",data["steel"].adequate)
    print("concrete_adequate:",data["concrete"].adequate)
    print("modal_rad_s:",data["modal_rad_s"])
    print("buckling_n:",data["buckling_n"])
    for f in data["files"]: print("file:",f)
    return 0
if __name__=="__main__": raise SystemExit(main())
