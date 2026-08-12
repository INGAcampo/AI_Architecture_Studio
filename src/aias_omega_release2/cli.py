"""Public module supporting the second Omega integrated product release."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from aias_omega_core.persistence import ProjectSerializer
from .reports import EngineeringReportService
from .validation import ProjectValidator
from .workflow import save_operational_outputs

def main() -> int:
    """Execute the public main operation for the second Omega integrated product release using explicit caller inputs."""
    parser = argparse.ArgumentParser(prog="aias-omega-r2")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor")

    demo = sub.add_parser("demo")
    demo.add_argument("--output-dir", default="omega_release_2_outputs")

    validate = sub.add_parser("validate")
    validate.add_argument("project_file")

    report = sub.add_parser("report")
    report.add_argument("project_file")

    args = parser.parse_args()

    if args.command == "doctor":
        print(json.dumps({
            "version": "2.0.0",
            "cad_to_bim_adapter": True,
            "structural_solver": True,
            "quantity_engine": True,
            "project_validation": True,
            "engineering_reports": True,
            "operational_workflow": True,
        }, indent=2))
        return 0

    if args.command == "demo":
        outputs = save_operational_outputs(Path(args.output_dir).resolve())
        for name, path in outputs.items():
            print(f"{name}: {path}")
        return 0

    project = ProjectSerializer().load(Path(args.project_file).resolve())

    if args.command == "validate":
        issues = ProjectValidator().validate(project)
        print(json.dumps([issue.__dict__ for issue in issues], indent=2))
        return 1 if issues else 0

    if args.command == "report":
        print(json.dumps(EngineeringReportService().summary(project), indent=2))
        return 0

    return 2

if __name__ == "__main__":
    raise SystemExit(main())
