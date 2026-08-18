"""Public module supporting foundation drawings, schedules and technical documentation."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import DocumentationPackage


class DocumentationWriter:
    """Execute the public DocumentationWriter operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    def write(self, package: DocumentationPackage, workspace: Path) -> dict[str, str]:
        """Persist write for foundation drawings, schedules and technical documentation in its stable external representation."""
        technical = workspace / "technical_file"
        technical.mkdir(parents=True, exist_ok=True)
        json_path = technical / "foundation_documentation.json"
        json_path.write_text(json.dumps(package.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        csv_path = technical / "bar_schedule.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["mark", "direction", "diameter_mm", "spacing_mm", "quantity", "length_mm", "layer", "weight_kg"])
            for bar in package.bar_schedule:
                writer.writerow([bar.mark, bar.direction, bar.diameter_mm, bar.spacing_mm, bar.quantity, bar.length_mm, bar.layer, f"{bar.total_weight_kg:.3f}"])
        md_path = technical / "FOUNDATION_TECHNICAL_REPORT.md"
        q = package.quantities
        rows = "\n".join(f"| {b.mark} | {b.direction} | {b.diameter_mm} | {b.spacing_mm} | {b.quantity} | {b.length_mm} | {b.total_weight_kg:.2f} |" for b in package.bar_schedule)
        md_path.write_text(
            f"# Foundation Technical Package - {package.foundation['name']}\n\n"
            f"Package: `{package.package_id}`\n\n## Reinforcement Schedule\n\n"
            "| Mark | Direction | Diameter mm | Spacing mm | Quantity | Length mm | Weight kg |\n|---|---:|---:|---:|---:|---:|---:|\n"
            f"{rows}\n\n## Quantities\n\n- Concrete: {q.concrete_m3:.4f} m3\n- Formwork: {q.formwork_m2:.4f} m2\n- Excavation: {q.excavation_m3:.4f} m3\n- Reinforcement: {q.reinforcement_kg:.3f} kg\n\n"
            "## Regulatory status\n\nREFERENCE_ONLY. A verified official code pack and professional review are mandatory before construction use.\n",
            encoding="utf-8",
        )
        return {"json": str(json_path), "csv": str(csv_path), "report": str(md_path)}
