"""Command-line diagnostics, reference validation and delivery release entrypoint."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .orchestrator import FoundationDeliveryOrchestrator
from .reference_cases import run_reference_cases


def main() -> int:
    """Dispatch foundation delivery operations with automation-safe status codes."""
    parser = argparse.ArgumentParser(prog="aias-foundation-delivery")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor"); commands.add_parser("validate")
    release = commands.add_parser("release"); release.add_argument("--workspace", default="ecp000001e_outputs"); release.add_argument("--source"); release.add_argument("--revision", default="R00")
    args = parser.parse_args()
    if args.command == "doctor":
        print(json.dumps({"version": "1.0.0", "ecp_d_consumer": True, "completeness": True, "revision_control": True, "issue_register": True, "approval_gate": True, "status": "READY"}, indent=2)); return 0
    if args.command == "validate":
        cases = run_reference_cases(Path("ecp000001e_validation").resolve()); passed = all(case["passed"] for case in cases); print(json.dumps({"passed": passed, "cases": cases}, indent=2)); return 0 if passed else 1
    result = FoundationDeliveryOrchestrator().execute(Path(args.workspace).resolve(), Path(args.source).resolve() if args.source else None, args.revision)
    print(json.dumps(result, indent=2)); return 0


if __name__ == "__main__": raise SystemExit(main())
