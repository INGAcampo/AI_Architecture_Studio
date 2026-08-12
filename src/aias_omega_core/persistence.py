"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
import json
from pathlib import Path
from .graph import Relationship
from .ids import ObjectId
from .materials import Material
from .objects import EngineeringObject
from .project import EngineeringProject

class ProjectSerializer:
    """Execute the public ProjectSerializer operation for the Omega application core and shared runtime services using explicit caller inputs."""
    SCHEMA_VERSION = 1

    def save(self, project: EngineeringProject, path: Path) -> None:
        """Persist save for the Omega application core and shared runtime services in its stable external representation."""
        data = {
            "schema_version": self.SCHEMA_VERSION,
            "name": project.name,
            "revision": project.revision,
            "objects": [
                {
                    "object_id": str(obj.object_id),
                    "object_type": obj.object_type,
                    "name": obj.name,
                    "geometry": obj.geometry,
                    "properties": obj.properties,
                    "material_id": obj.material_id,
                    "layer": obj.layer,
                    "classification": obj.classification,
                    "metadata": obj.metadata,
                    "revision": obj.revision,
                }
                for obj in project.objects.values()
            ],
            "relationships": [
                {
                    "source": str(rel.source),
                    "target": str(rel.target),
                    "relation_type": rel.relation_type,
                }
                for rel in project.graph.all()
            ],
            "materials": [
                {
                    "material_id": material.material_id,
                    "name": material.name,
                    "category": material.category,
                    "properties": material.properties,
                }
                for material in project.materials.all()
            ],
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self, path: Path) -> EngineeringProject:
        """Load load for the Omega application core and shared runtime services while preserving typed state."""
        data = json.loads(path.read_text(encoding="utf-8"))
        project = EngineeringProject(data["name"], path=path)
        for row in data.get("objects", []):
            obj = EngineeringObject(
                object_id=ObjectId.parse(row["object_id"]),
                object_type=row["object_type"],
                name=row.get("name", ""),
                geometry=row.get("geometry", {}),
                properties=row.get("properties", {}),
                material_id=row.get("material_id"),
                layer=row.get("layer", "0"),
                classification=row.get("classification", ""),
                metadata=row.get("metadata", {}),
                revision=row.get("revision", 0),
            )
            project.objects[obj.object_id] = obj
        for row in data.get("relationships", []):
            project.graph.add(Relationship(
                ObjectId.parse(row["source"]),
                ObjectId.parse(row["target"]),
                row["relation_type"],
            ))
        for row in data.get("materials", []):
            project.materials.add(Material(
                row["material_id"],
                row["name"],
                row["category"],
                row.get("properties", {}),
            ))
        project.revision = data.get("revision", 0)
        return project
