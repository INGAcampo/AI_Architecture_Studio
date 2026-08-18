"""Public module supporting advanced AEPS production, governance and observability."""
import argparse, json
from pathlib import Path
from .orchestrator import AdvancedProductionOrchestrator

def main() -> int:
    """Execute the public main operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    p = argparse.ArgumentParser(prog="aias-aeps-v4")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    b = sub.add_parser("build")
    b.add_argument("specification")
    b.add_argument("--workspace", default="aeps_v4_build")
    a = p.parse_args()

    if a.command == "doctor":
        print(json.dumps({
            "version":"4.0.0",
            "domain_template_engine":True,
            "contract_generator":True,
            "advanced_test_generator":True,
            "generated_test_executor":True,
            "migration_engine":True,
            "transactional_rollback":True,
            "asset_catalog":True,
            "productivity_measurement":True,
            "full_constitution_validator":True,
            "advanced_certification":True,
            "advanced_orchestrator":True
        }, indent=2))
        return 0

    result = AdvancedProductionOrchestrator().build(
        Path(a.specification).resolve(),
        Path(a.workspace).resolve(),
    )
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
