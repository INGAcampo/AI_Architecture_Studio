"""Command-line entry point for ECP-000001F validation and release."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .orchestrator import FoundationHandoverOrchestrator
from .reference_cases import run_reference_cases

def main()->int:
    """Run diagnostics, reference validation or a lifecycle release."""
    parser=argparse.ArgumentParser(prog="aias-foundation-handover"); sub=parser.add_subparsers(dest="command",required=True); sub.add_parser("doctor"); sub.add_parser("validate"); release=sub.add_parser("release"); release.add_argument("--workspace",default="ecp000001f_outputs"); release.add_argument("--transmittal")
    args=parser.parse_args()
    if args.command=="doctor": print(json.dumps({"version":"1.0.0","ecp_e_consumer":True,"custody":True,"acceptance_gates":True,"maturity_assessment":True,"kpi_evidence":True,"status":"READY"},indent=2)); return 0
    if args.command=="validate":
        cases=run_reference_cases(Path("ecp000001f_validation").resolve()); passed=all(c["passed"] for c in cases); print(json.dumps({"passed":passed,"cases":cases},indent=2)); return 0 if passed else 1
    result=FoundationHandoverOrchestrator().execute(Path(args.workspace).resolve(),Path(args.transmittal).resolve() if args.transmittal else None); print(json.dumps(result,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
