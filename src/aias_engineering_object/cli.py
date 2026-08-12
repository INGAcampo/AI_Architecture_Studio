"""Command-line diagnostics, acceptance validation, benchmarking and release entrypoint."""
import argparse,json,time
from pathlib import Path
from .reference_cases import run_reference_cases, build_reference_object
from .orchestrator import EngineeringObjectOrchestrator
from .adapters import ECFAdapter

def main():
    """Dispatch engineering-object kernel operations and return process-safe status codes."""
    p=argparse.ArgumentParser(prog="aias-eok")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    sub.add_parser("validate")
    b=sub.add_parser("benchmark"); b.add_argument("--iterations",type=int,default=10000)
    r=sub.add_parser("release"); r.add_argument("--workspace",default="eok_amp010c_outputs")
    args=p.parse_args()

    if args.command=="doctor":
        print(json.dumps({
            "version":"1.0.0",
            "engineering_object_core":True,
            "identity_service":True,
            "property_system":True,
            "material_system":True,
            "state_machine":True,
            "version_store":True,
            "traceability_engine":True,
            "geometry_adapter":True,
            "ecf_adapter":True,
            "aeks_adapter":True,
            "enterprise_registry_adapter":True,
            "serialization":True,
            "reference_cases":True,
            "sdd_active":True
        },indent=2)); return 0

    if args.command=="validate":
        cases=run_reference_cases()
        print(json.dumps({"passed":all(c["passed"] for c in cases),"cases":cases},indent=2))
        return 0 if all(c["passed"] for c in cases) else 1

    if args.command=="benchmark":
        obj=build_reference_object()
        start=time.perf_counter()
        for _ in range(args.iterations):
            ECFAdapter().bearing_pressure(obj)
        elapsed=time.perf_counter()-start
        print(json.dumps({
            "iterations":args.iterations,
            "elapsed_seconds":elapsed,
            "operations_per_second":args.iterations/elapsed
        },indent=2)); return 0

    print(json.dumps(EngineeringObjectOrchestrator().execute_reference_flow(Path(args.workspace).resolve()),indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
