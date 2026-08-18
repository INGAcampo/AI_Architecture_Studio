"""Public module supporting the AIAS continuity and context system."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .builder import ContextBuilder
from .storage import ContextStore
from .validator import ContextValidator
from .continuity import create_continuity_package, validate_continuity_package


def main() -> int:
    """Execute the public main operation for the AIAS continuity and context system using explicit caller inputs."""
    parser = argparse.ArgumentParser(prog="aias-context-engine")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    build = commands.add_parser("build")
    build.add_argument("--project-root", default=".")
    build.add_argument("--output", default="ACKC")
    validate = commands.add_parser("validate")
    validate.add_argument("--context", default="ACKC/MASTER_CONTEXT.json")
    show = commands.add_parser("show")
    show.add_argument("--context", default="ACKC/MASTER_CONTEXT.json")
    handoff = commands.add_parser("handoff")
    handoff.add_argument("--ackc", default="ACKC")
    handoff.add_argument("--output", default="ACKC/AIAS_CONTINUITY_HANDOFF.zip")
    verify_handoff = commands.add_parser("verify-handoff")
    verify_handoff.add_argument("--package", default="ACKC/AIAS_CONTINUITY_HANDOFF.zip")
    args = parser.parse_args()

    if args.command == "doctor":
        print(json.dumps({"engine": "ACE", "version": "1.0.0", "schema": "1.0.0", "snapshotting": True, "integrity": "SHA-256", "status": "READY"}, indent=2))
        return 0
    if args.command == "build":
        project_root = Path(args.project_root).resolve()
        context = ContextBuilder(project_root).build()
        paths = ContextStore((project_root / args.output).resolve()).write(context)
        validation = ContextValidator().validate(context)
        print(json.dumps({"paths": paths, "validation": validation}, indent=2))
        return 0 if validation["valid"] else 1
    if args.command == "validate":
        result = ContextValidator().validate_file(Path(args.context).resolve())
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1
    if args.command == "handoff":
        result = create_continuity_package(Path(args.ackc).resolve(), Path(args.output).resolve())
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "verify-handoff":
        result = validate_continuity_package(Path(args.package).resolve())
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1
    data = json.loads(Path(args.context).resolve().read_text(encoding="utf-8"))
    print(json.dumps({"identity": data["identity"], "current_state": data["current_state"], "roadmap": data["roadmap"], "integrity": data["integrity"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
