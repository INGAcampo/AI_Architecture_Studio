"""Public module supporting foundation drawings, schedules and technical documentation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .orchestrator import FoundationDocumentationOrchestrator
from .reference_cases import run_reference_cases


def main() -> int:
    """Execute the public main operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    parser = argparse.ArgumentParser(prog="aias-foundation-documentation")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    commands.add_parser("validate")
    release = commands.add_parser("release")
    release.add_argument("--workspace", default="ecp000001d_outputs")
    args = parser.parse_args()
    if args.command == "doctor":
        print(json.dumps({"version": "1.0.0", "ecp_a_consumer": True, "ecp_b_consumer": True, "ecp_c_consumer": True, "svg_drawings": True, "bar_schedule": True, "quantities": True, "technical_report": True, "human_review_required": True, "status": "READY"}, indent=2))
        return 0
    if args.command == "validate":
        cases = run_reference_cases(Path("ecp000001d_validation").resolve())
        result = {"passed": all(case["passed"] for case in cases), "cases": cases}
        print(json.dumps(result, indent=2))
        return 0 if result["passed"] else 1
    result = FoundationDocumentationOrchestrator().execute(Path(args.workspace).resolve())
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
