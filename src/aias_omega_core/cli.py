"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from .persistence import ProjectSerializer
from .workflows import create_cad_to_bim_to_structural_demo

def main() -> int:
    """Execute the public main operation for the Omega application core and shared runtime services using explicit caller inputs."""
    parser = argparse.ArgumentParser(prog="aias-omega")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor")
    demo = sub.add_parser("demo")
    demo.add_argument("--output", default="aias_omega_demo.aias.json")

    inspect = sub.add_parser("inspect")
    inspect.add_argument("project_file")

    args = parser.parse_args()

    if args.command == "doctor":
        print(json.dumps({
            "version": "1.0.0",
            "core": True,
            "project_engine": True,
            "object_graph": True,
            "event_bus": True,
            "command_bus": True,
            "transactions": True,
            "selection": True,
            "units": True,
            "materials": True,
            "plugins": True,
            "persistence": True,
        }, indent=2))
        return 0

    if args.command == "demo":
        project = create_cad_to_bim_to_structural_demo()
        path = Path(args.output).resolve()
        ProjectSerializer().save(project, path)
        print(f"Project: {path}")
        print(f"Objects: {len(project.objects)}")
        print(f"Relationships: {len(project.graph.all())}")
        print("Workflow: CAD -> BIM -> Structural -> Quantity")
        return 0

    if args.command == "inspect":
        project = ProjectSerializer().load(Path(args.project_file).resolve())
        print(json.dumps({
            "name": project.name,
            "revision": project.revision,
            "objects": len(project.objects),
            "relationships": len(project.graph.all()),
            "materials": len(project.materials.all()),
            "types": sorted({obj.object_type for obj in project.objects.values()}),
        }, indent=2))
        return 0

    return 2

if __name__ == "__main__":
    raise SystemExit(main())
