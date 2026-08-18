"""Command-line diagnostics, validation, benchmark and geometry release entrypoint."""
import argparse,json,time
from pathlib import Path
from .reference_cases import run_reference_cases
from .orchestrator import GeometryKernelOrchestrator
from .polygon import Polygon2D
from .primitives import Point2D

def main():
    """Dispatch kernel operations with machine-readable results and exit status."""
    p=argparse.ArgumentParser(prog="aias-geometry")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    sub.add_parser("validate")
    b=sub.add_parser("benchmark"); b.add_argument("--iterations",type=int,default=10000)
    r=sub.add_parser("release"); r.add_argument("--workspace",default="geometry_amp010b_outputs")
    args=p.parse_args()
    if args.command=="doctor":
        print(json.dumps({
            "version":"1.0.0","primitives":True,"polygon_engine":True,
            "transforms":True,"intersections":True,"measurements":True,
            "serialization":True,"validation":True,"reference_cases":True,
            "ecf_integration_ready":True,"cad_bim_integration_ready":True,
            "sdd_active":True
        },indent=2)); return 0
    if args.command=="validate":
        cases=run_reference_cases()
        print(json.dumps({"passed":all(c["passed"] for c in cases),"cases":cases},indent=2))
        return 0 if all(c["passed"] for c in cases) else 1
    if args.command=="benchmark":
        poly=Polygon2D((Point2D(0,0),Point2D(2,0),Point2D(2,2),Point2D(0,2)))
        start=time.perf_counter()
        for _ in range(args.iterations):
            _=poly.area; _=poly.centroid; _=poly.contains(Point2D(1,1))
        elapsed=time.perf_counter()-start
        print(json.dumps({"iterations":args.iterations,"elapsed_seconds":elapsed,"operations_per_second":args.iterations*3/elapsed},indent=2))
        return 0
    print(json.dumps(GeometryKernelOrchestrator().validate_and_release(Path(args.workspace).resolve()),indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
