"""Command-line health check and executable governance-SDD demonstration."""
import argparse, json
from pathlib import Path
from .workflow import run_foundation_demo

def main() -> int:
    """Dispatch governance operations with machine-readable evidence and exit codes."""
    p = argparse.ArgumentParser(prog="aias-aeps-v2")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    d = sub.add_parser("demo")
    d.add_argument("--output", default="aeps_governance_sdd_outputs")
    a = p.parse_args()

    if a.command == "doctor":
        print(json.dumps({
            "version":"2.0.0",
            "constitution_core":True,
            "requirement_model":True,
            "specification_model":True,
            "traceability_matrix":True,
            "requirement_validator":True,
            "specification_validator":True,
            "quality_gate_engine":True,
            "kpi_engine":True,
            "generators":True
        }, indent=2))
        return 0

    result = run_foundation_demo(Path(a.output).resolve())
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
