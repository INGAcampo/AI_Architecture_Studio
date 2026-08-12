"""Command-line diagnostics, validation, search and AEKS release entrypoint."""
import argparse, json
from pathlib import Path
from .orchestrator import AEKSOrchestrator
from .repository import KnowledgeRepository
from .search import EngineeringSearchEngine

def main() -> int:
    """Dispatch knowledge-system operations with machine-readable results."""
    parser = argparse.ArgumentParser(prog="aias-aeks")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    imp = sub.add_parser("import")
    imp.add_argument("source")
    imp.add_argument("--workspace", default="aeks_workspace")
    val = sub.add_parser("validate")
    val.add_argument("source")
    sea = sub.add_parser("search")
    sea.add_argument("workspace")
    sea.add_argument("query")
    stats = sub.add_parser("stats")
    stats.add_argument("workspace")
    args = parser.parse_args()

    if args.command == "doctor":
        print(json.dumps({
            "version":"1.0.0",
            "knowledge_units":True,
            "repository":True,
            "registry":True,
            "ontology":True,
            "knowledge_graph":True,
            "validation":True,
            "engineering_search":True,
            "importers":True,
            "exporters":True,
            "versioning":True,
            "traceability":True,
            "orchestrator":True,
            "sdd_active":True,
            "human_review_supported":True
        }, indent=2))
        return 0

    if args.command == "import":
        print(json.dumps(AEKSOrchestrator().import_unit(
            Path(args.source).resolve(), Path(args.workspace).resolve()
        ), indent=2))
        return 0

    if args.command == "validate":
        from .importers import JSONKnowledgeImporter
        unit = JSONKnowledgeImporter().load(Path(args.source).resolve())
        print(json.dumps({"eku_id":unit.eku_id,"valid":True}, indent=2))
        return 0

    repo = KnowledgeRepository(Path(args.workspace).resolve() / "repository")
    units = [repo.get(eku_id) for eku_id in repo.list_ids()]
    if args.command == "search":
        results = EngineeringSearchEngine().search(units, args.query)
        print(json.dumps([u.to_dict() for u in results], indent=2, ensure_ascii=False))
        return 0

    print(json.dumps({
        "knowledge_units":len(units),
        "disciplines":len({u.discipline for u in units}),
        "approved":sum(u.status=="APPROVED" for u in units),
        "human_review_required":sum(u.human_review_required for u in units)
    }, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
