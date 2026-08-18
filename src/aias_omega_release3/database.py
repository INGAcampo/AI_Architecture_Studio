"""Public module supporting the third Omega integrated product release."""
from __future__ import annotations
import json
import sqlite3
import time
from pathlib import Path
from aias_omega_core.ids import ObjectId
from aias_omega_core.objects import EngineeringObject
from aias_omega_core.project import EngineeringProject
from aias_omega_core.materials import Material
from aias_omega_core.graph import Relationship

SCHEMA_VERSION = 1

class ProjectDatabase:
    """Execute the public ProjectDatabase operation for the third Omega integrated product release using explicit caller inputs."""
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self):
        """Execute the public ProjectDatabase.connect operation for the third Omega integrated product release using explicit caller inputs."""
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        return con

    def initialize(self) -> None:
        """Execute the public ProjectDatabase.initialize operation for the third Omega integrated product release using explicit caller inputs."""
        with self.connect() as con:
            con.executescript("""
            PRAGMA foreign_keys=ON;
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS objects(
                object_id TEXT PRIMARY KEY,
                object_type TEXT NOT NULL,
                name TEXT NOT NULL,
                geometry_json TEXT NOT NULL,
                properties_json TEXT NOT NULL,
                material_id TEXT,
                layer TEXT NOT NULL,
                classification TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                revision INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS relationships(
                source TEXT NOT NULL,
                target TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                PRIMARY KEY(source,target,relation_type)
            );
            CREATE TABLE IF NOT EXISTS materials(
                material_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                properties_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_log(
                audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                object_id TEXT,
                details_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS snapshots(
                snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                label TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );
            """)
            con.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('schema_version',?)", (str(SCHEMA_VERSION),))

    def save_project(self, project: EngineeringProject) -> None:
        """Persist project for the third Omega integrated product release in its stable external representation."""
        self.initialize()
        with self.connect() as con:
            con.execute("DELETE FROM objects")
            con.execute("DELETE FROM relationships")
            con.execute("DELETE FROM materials")
            for obj in project.objects.values():
                con.execute("""
                    INSERT INTO objects VALUES(?,?,?,?,?,?,?,?,?,?)
                """, (
                    str(obj.object_id), obj.object_type, obj.name,
                    json.dumps(obj.geometry), json.dumps(obj.properties),
                    obj.material_id, obj.layer, obj.classification,
                    json.dumps(obj.metadata), obj.revision,
                ))
            for rel in project.graph.all():
                con.execute("INSERT INTO relationships VALUES(?,?,?)",
                            (str(rel.source), str(rel.target), rel.relation_type))
            for mat in project.materials.all():
                con.execute("INSERT INTO materials VALUES(?,?,?,?)",
                            (mat.material_id, mat.name, mat.category, json.dumps(mat.properties)))
            con.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('project_name',?)", (project.name,))
            con.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('project_revision',?)", (str(project.revision),))
            con.execute("INSERT INTO audit_log(timestamp,action,object_id,details_json) VALUES(?,?,?,?)",
                        (time.strftime("%Y-%m-%dT%H:%M:%S"), "save_project", None,
                         json.dumps({"objects": len(project.objects)})))

    def load_project(self) -> EngineeringProject:
        """Load project for the third Omega integrated product release while preserving typed state."""
        self.initialize()
        with self.connect() as con:
            meta = {r["key"]: r["value"] for r in con.execute("SELECT key,value FROM meta")}
            project = EngineeringProject(meta.get("project_name", "Untitled"), path=self.path)
            for row in con.execute("SELECT * FROM materials"):
                project.materials.add(Material(row["material_id"], row["name"], row["category"],
                                               json.loads(row["properties_json"])))
            for row in con.execute("SELECT * FROM objects"):
                obj = EngineeringObject(
                    object_id=ObjectId.parse(row["object_id"]),
                    object_type=row["object_type"],
                    name=row["name"],
                    geometry=json.loads(row["geometry_json"]),
                    properties=json.loads(row["properties_json"]),
                    material_id=row["material_id"],
                    layer=row["layer"],
                    classification=row["classification"],
                    metadata=json.loads(row["metadata_json"]),
                    revision=row["revision"],
                )
                project.objects[obj.object_id] = obj
            for row in con.execute("SELECT * FROM relationships"):
                project.graph.add(Relationship(
                    ObjectId.parse(row["source"]), ObjectId.parse(row["target"]), row["relation_type"]
                ))
            project.revision = int(meta.get("project_revision", 0))
            return project

    def append_audit(self, action: str, object_id: str | None = None, details: dict | None = None) -> None:
        """Execute the public ProjectDatabase.append_audit operation for the third Omega integrated product release using explicit caller inputs."""
        self.initialize()
        with self.connect() as con:
            con.execute("INSERT INTO audit_log(timestamp,action,object_id,details_json) VALUES(?,?,?,?)",
                        (time.strftime("%Y-%m-%dT%H:%M:%S"), action, object_id, json.dumps(details or {})))

    def audit_entries(self) -> tuple[dict, ...]:
        """Execute the public ProjectDatabase.audit_entries operation for the third Omega integrated product release using explicit caller inputs."""
        self.initialize()
        with self.connect() as con:
            return tuple(dict(row) for row in con.execute("SELECT * FROM audit_log ORDER BY audit_id"))

    def create_snapshot(self, project: EngineeringProject, label: str) -> int:
        """Build the snapshot required by the third Omega integrated product release from explicit inputs."""
        payload = {
            "name": project.name,
            "revision": project.revision,
            "objects": [
                {
                    "object_id": str(o.object_id), "object_type": o.object_type, "name": o.name,
                    "geometry": o.geometry, "properties": o.properties, "material_id": o.material_id,
                    "layer": o.layer, "classification": o.classification, "metadata": o.metadata,
                    "revision": o.revision,
                } for o in project.objects.values()
            ],
        }
        self.initialize()
        with self.connect() as con:
            cursor = con.execute("INSERT INTO snapshots(timestamp,label,payload_json) VALUES(?,?,?)",
                                 (time.strftime("%Y-%m-%dT%H:%M:%S"), label, json.dumps(payload)))
            return int(cursor.lastrowid)

    def list_snapshots(self) -> tuple[dict, ...]:
        """Return snapshots from the third Omega integrated product release using deterministic lookup rules."""
        self.initialize()
        with self.connect() as con:
            return tuple(dict(row) for row in con.execute(
                "SELECT snapshot_id,timestamp,label FROM snapshots ORDER BY snapshot_id"
            ))
