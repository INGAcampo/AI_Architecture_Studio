"""Command-line diagnostics, acceptance validation and release generation."""
import argparse,json
from pathlib import Path
from .reference_cases import run_reference_cases
from .orchestrator import FoundationCalculationOrchestrator

def main():
    """Dispatch foundation calculation operations with automation-safe exit codes."""
    p=argparse.ArgumentParser(prog="aias-foundation-calcs")
    s=p.add_subparsers(dest="cmd",required=True)
    s.add_parser("doctor"); s.add_parser("validate")
    r=s.add_parser("release"); r.add_argument("--workspace",default="ecp000001b_outputs")
    a=p.parse_args()
    if a.cmd=="doctor":
        print(json.dumps({
            "version":"1.0.0",
            "load_combination_engine":True,
            "bearing_pressure_engine":True,
            "eccentricity_and_kern":True,
            "one_way_shear_demand":True,
            "punching_shear_demand":True,
            "flexural_demand":True,
            "elastic_settlement_estimate":True,
            "report_writer":True,
            "aeks_code_pack_required_for_capacity":True,
            "human_review_required":True,
            "sdd_active":True
        },indent=2)); return 0
    if a.cmd=="validate":
        cases=run_reference_cases()
        print(json.dumps({"passed":all(c["passed"] for c in cases),"cases":cases},indent=2))
        return 0 if all(c["passed"] for c in cases) else 1
    print(json.dumps(FoundationCalculationOrchestrator().execute(Path(a.workspace).resolve()),indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
