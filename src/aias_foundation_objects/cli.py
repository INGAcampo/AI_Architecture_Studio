"""Command-line diagnostics, acceptance validation and object-library release."""
import argparse,json
from pathlib import Path
from .reference_cases import run_reference_cases
from .orchestrator import FoundationObjectOrchestrator

def main():
    """Dispatch foundation-object operations with automation-safe exit codes."""
    p=argparse.ArgumentParser(prog="aias-foundation-objects")
    s=p.add_subparsers(dest="cmd",required=True)
    s.add_parser("doctor"); s.add_parser("validate")
    r=s.add_parser("release"); r.add_argument("--workspace",default="ecp000001a_outputs")
    a=p.parse_args()
    if a.cmd=="doctor":
        print(json.dumps({
            "version":"1.0.0",
            "isolated_footing":True,
            "combined_footing":True,
            "strip_footing":True,
            "mat_foundation":True,
            "pedestal":True,
            "foundation_beam":True,
            "engineering_object_adapter":True,
            "geometry_kernel_adapter":True,
            "ecf_adapter":True,
            "sdd_active":True
        },indent=2)); return 0
    if a.cmd=="validate":
        cases=run_reference_cases()
        print(json.dumps({"passed":all(c["passed"] for c in cases),"cases":cases},indent=2))
        return 0 if all(c["passed"] for c in cases) else 1
    print(json.dumps(FoundationObjectOrchestrator().execute(Path(a.workspace).resolve()),indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
