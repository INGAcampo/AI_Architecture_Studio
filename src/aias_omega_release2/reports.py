"""Public module supporting the second Omega integrated product release."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from aias_omega_core.project import EngineeringProject

class EngineeringReportService:
    """Execute the public EngineeringReportService operation for the second Omega integrated product release using explicit caller inputs."""
    def summary(self, project: EngineeringProject) -> dict:
        """Execute the public EngineeringReportService.summary operation for the second Omega integrated product release using explicit caller inputs."""
        by_type = {}
        total_cost = 0.0
        max_displacement = 0.0

        for obj in project.objects.values():
            by_type[obj.object_type] = by_type.get(obj.object_type, 0) + 1
            if obj.object_type == "quantity_item":
                total_cost += float(obj.properties.get("total_cost", 0.0))
            if obj.object_type == "structural_member":
                max_displacement = max(
                    max_displacement,
                    abs(float(obj.properties.get("displacement_m", 0.0))),
                )

        return {
            "project_name": project.name,
            "revision": project.revision,
            "object_count": len(project.objects),
            "relationship_count": len(project.graph.all()),
            "objects_by_type": by_type,
            "total_cost": total_cost,
            "max_structural_displacement_m": max_displacement,
        }

    def export_json(self, project: EngineeringProject, path: Path) -> None:
        """Persist json for the second Omega integrated product release in its stable external representation."""
        path.write_text(json.dumps(self.summary(project), indent=2), encoding="utf-8")

    def export_objects_csv(self, project: EngineeringProject, path: Path) -> None:
        """Persist objects csv for the second Omega integrated product release in its stable external representation."""
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(["object_id", "type", "name", "material_id", "classification"])
            for obj in project.objects.values():
                writer.writerow([
                    str(obj.object_id),
                    obj.object_type,
                    obj.name,
                    obj.material_id or "",
                    obj.classification,
                ])

    def markdown(self, project: EngineeringProject) -> str:
        """Execute the public EngineeringReportService.markdown operation for the second Omega integrated product release using explicit caller inputs."""
        summary = self.summary(project)
        rows = [
            f"# Engineering Report — {summary['project_name']}",
            "",
            f"- Revision: {summary['revision']}",
            f"- Objects: {summary['object_count']}",
            f"- Relationships: {summary['relationship_count']}",
            f"- Total cost: {summary['total_cost']:.2f}",
            f"- Maximum structural displacement: {summary['max_structural_displacement_m']:.8f} m",
            "",
            "## Objects by type",
            "",
        ]
        for key, value in sorted(summary["objects_by_type"].items()):
            rows.append(f"- {key}: {value}")
        return "\n".join(rows)
