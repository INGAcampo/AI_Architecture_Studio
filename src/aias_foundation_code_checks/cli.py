"""Command-line diagnostics, acceptance validation and code-check release entrypoint."""
import argparse,json
from pathlib import Path
from .reference_cases import run_reference_cases
from .orchestrator import FoundationCodeCheckOrchestrator

def main():
    """Dispatch framework operations and communicate validation through exit status."""
    p=argparse.ArgumentParser(prog="aias-foundation-code-checks")
    s=p.add_subparsers(dest="cmd",required=True)
    s.add_parser("doctor"); s.add_parser("validate")
    r=s.add_parser("release"); r.add_argument("--workspace",default="ecp000001c_outputs")
    a=p.parse_args()
    if a.cmd=="doctor":
        print(json.dumps({
            "version":"1.0.0",
            "code_pack_registry":True,
            "parameter_driven_checks":True,
            "flexure_design":True,
            "one_way_shear_check":True,
            "punching_shear_check":True,
            "cover_check":True,
            "thickness_check":True,
            "report_writer":True,
            "generic_reference_pack":True,
            "verified_official_pack_required_for_regulated_use":True,
            "human_review_required":True,
            "sdd_active":True
        },indent=2)); return 0
    if a.cmd=="validate":
        cases=run_reference_cases()
        print(json.dumps({"passed":all(c["passed"] for c in cases),"cases":cases},indent=2))
        return 0 if all(c["passed"] for c in cases) else 1
    print(json.dumps(FoundationCodeCheckOrchestrator().execute(Path(a.workspace).resolve()),indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
