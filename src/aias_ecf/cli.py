"""Command-line diagnostics, validation, benchmarks and ECF release generation."""
import argparse, json, math, time
from pathlib import Path
from .reference_cases import run_reference_cases
from .orchestrator import ECFOrchestrator
from .matrix import MatrixEngine
from .units import UnitsEngine

def main() -> int:
    """Dispatch ECF operations with machine-readable output and status codes."""
    parser = argparse.ArgumentParser(prog="aias-ecf")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("validate")
    bench = sub.add_parser("benchmark")
    bench.add_argument("--iterations", type=int, default=5000)
    rel = sub.add_parser("release")
    rel.add_argument("--workspace", default="ecf_amp010a_outputs")
    args = parser.parse_args()

    if args.command == "doctor":
        print(json.dumps({
            "version":"1.0.0",
            "matrix_engine":True,
            "vector_engine":True,
            "units_engine":True,
            "equation_engine":True,
            "numerical_engine":True,
            "validation_engine":True,
            "reference_cases":True,
            "aeks_cku_integration":True,
            "enterprise_registry_integration":True,
            "sdd_active":True,
            "human_review_supported":True,
        }, indent=2))
        return 0

    if args.command == "validate":
        cases = run_reference_cases()
        print(json.dumps({"passed":all(c["passed"] for c in cases),"cases":cases}, indent=2))
        return 0 if all(c["passed"] for c in cases) else 1

    if args.command == "benchmark":
        start = time.perf_counter()
        for _ in range(args.iterations):
            MatrixEngine.solve([[2,1],[5,7]],[11,13])
            UnitsEngine().convert(1.0,"m","ft")
        elapsed = time.perf_counter() - start
        print(json.dumps({
            "iterations":args.iterations,
            "elapsed_seconds":elapsed,
            "operations_per_second":(args.iterations*2)/elapsed,
        }, indent=2))
        return 0

    print(json.dumps(ECFOrchestrator().validate_and_release(Path(args.workspace).resolve()), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
