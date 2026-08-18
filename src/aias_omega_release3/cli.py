"""Public module supporting the third Omega integrated product release."""
import argparse, json
from pathlib import Path
from aias_omega_release2.workflow import build_operational_project
from .database import ProjectDatabase
from .repository import ProjectRepository

def main():
    """Execute the public main operation for the third Omega integrated product release using explicit caller inputs."""
    p=argparse.ArgumentParser(prog="aias-omega-r3")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    demo=sub.add_parser("demo"); demo.add_argument("--output",default="omega_release_3_project.aias.db")
    inspect=sub.add_parser("inspect"); inspect.add_argument("database")
    a=p.parse_args()
    if a.command=="doctor":
        print(json.dumps({"version":"3.0.0","sqlite_database":True,"audit_log":True,"snapshots":True},indent=2)); return 0
    if a.command=="demo":
        project=build_operational_project()
        path=Path(a.output).resolve()
        repo=ProjectRepository(); repo.save(project,path); repo.snapshot(project,"Initial coordinated model")
        print("database:",path); print("objects:",len(project.objects)); print("snapshots:",len(ProjectDatabase(path).list_snapshots())); return 0
    db=ProjectDatabase(Path(a.database).resolve()); project=db.load_project()
    print(json.dumps({"name":project.name,"objects":len(project.objects),"relationships":len(project.graph.all()),
                      "audit_entries":len(db.audit_entries()),"snapshots":len(db.list_snapshots())},indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
