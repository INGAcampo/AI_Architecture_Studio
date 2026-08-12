import pytest
from aias_omega_release2.workflow import build_operational_project
from aias_omega_release3.database import ProjectDatabase
from aias_omega_release3.repository import ProjectRepository

@pytest.mark.parametrize("i", range(200))
def test_database_roundtrip(tmp_path, i):
    path=tmp_path/f"p_{i}.db"
    project=build_operational_project()
    ProjectRepository().save(project,path)
    restored=ProjectRepository().open(path)
    assert len(restored.objects)==4
    assert len(restored.graph.all())==3
    assert restored.name=="Omega Operational Demo"

@pytest.mark.parametrize("i", range(100))
def test_audit_and_snapshot(tmp_path, i):
    path=tmp_path/f"a_{i}.db"
    project=build_operational_project()
    db=ProjectDatabase(path); db.save_project(project)
    db.append_audit("custom",details={"i":i})
    sid=db.create_snapshot(project,f"S{i}")
    assert sid>=1
    assert len(db.audit_entries())==2
    assert db.list_snapshots()[0]["label"]==f"S{i}"
