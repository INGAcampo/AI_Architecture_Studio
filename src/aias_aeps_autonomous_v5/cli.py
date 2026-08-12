"""Public module supporting autonomous engineering planning and controlled execution."""
import argparse, json
from pathlib import Path
from .orchestrator import AutonomousEngineeringOrchestrator

def main() -> int:
    """Execute the public main operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    parser = argparse.ArgumentParser(prog="aias-aeps-v5")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    build = sub.add_parser("build")
    build.add_argument("specification")
    build.add_argument("--workspace", default="aeps_v5_build")
    args = parser.parse_args()

    if args.command == "doctor":
        print(json.dumps({
            "version":"5.0.0",
            "persistent_asset_catalog":True,
            "automatic_asset_reuse":True,
            "intelligent_template_selection":True,
            "pipeline_planner":True,
            "incremental_execution":True,
            "compilation_cache":True,
            "parallel_execution":True,
            "observability":True,
            "security_policies":True,
            "multidomain_program_generator":True,
            "workspace_test_runner":True,
            "autonomous_certification":True,
            "autonomous_orchestrator":True
        }, indent=2))
        return 0

    result = AutonomousEngineeringOrchestrator().build(
        Path(args.specification).resolve(),
        Path(args.workspace).resolve(),
    )
    print(json.dumps({
        "certified": result.certified,
        "cache_hit": result.cache_hit,
        "artifacts": [str(p) for p in result.artifacts],
        "reports": result.reports,
    }, indent=2, default=str))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
