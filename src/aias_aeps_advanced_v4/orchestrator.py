"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from pathlib import Path
import json, zipfile, hashlib
from .catalog import EngineeringAssetCatalog
from .templates import default_templates
from .generation import DomainTemplateEngine, safe_identifier
from .contracts import ContractGenerator
from .test_generation import AdvancedTestGenerator
from .test_execution import GeneratedTestExecutor
from .transactions import FileTransaction
from .productivity import ProductivityMeasurementEngine
from .certification import AdvancedCertificationEngine

class AdvancedProductionOrchestrator:
    """Execute the public AdvancedProductionOrchestrator operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    def build(self, spec_file: Path, workspace: Path) -> dict:
        """Build the build required by advanced AEPS production, governance and observability from explicit inputs."""
        data = json.loads(spec_file.read_text(encoding="utf-8"))
        catalog = EngineeringAssetCatalog()
        for template in default_templates():
            catalog.register_template(template)

        module_name = data["module_name"]
        class_name = safe_identifier(data.get("class_name", module_name.title().replace("_", "")))
        template = catalog.get_template(data.get("template_id", "TPL-000001"))

        tx = FileTransaction(workspace, workspace.with_name(workspace.name + "_backup"))
        tx.begin()
        try:
            generated = DomainTemplateEngine().render(
                template,
                {
                    "module_name": module_name,
                    "class_name": class_name,
                    "domain": data.get("domain", "generic"),
                    "version": data.get("version", "1.0.0"),
                },
                workspace,
            )
            ContractGenerator().generate(module_name, class_name, workspace)
            AdvancedTestGenerator().generate(module_name, class_name, workspace)

            test_result = GeneratedTestExecutor().run(workspace)
            productivity = ProductivityMeasurementEngine().measure(
                baseline_hours=float(data.get("baseline_hours", 100)),
                manual_hours=float(data.get("manual_hours", 45)),
                automation_hours_saved=float(data.get("automation_hours_saved", 40)),
                reuse_hours_saved=float(data.get("reuse_hours_saved", 15)),
                quality_passed=test_result.passed,
            )

            traceability_coverage = 1.0 if data.get("requirements") else 0.0
            context = {
                "specification_id": data.get("id"),
                "requirements": data.get("requirements", []),
                "adr_refs": data.get("adr_refs", []),
                "architecture_refs": data.get("architecture_refs", []),
                "tests_passed": test_result.passed,
                "traceability_coverage": traceability_coverage,
                "quality_passed": test_result.passed,
                "time_reduction": productivity.reduction_ratio,
            }

            cert = AdvancedCertificationEngine().certify(context, workspace / "certification")
            if not cert.certified:
                raise RuntimeError(f"Certification failed: {cert.issues}")

            release_dir = workspace / "release"
            release_dir.mkdir(parents=True, exist_ok=True)
            archive = release_dir / f"{data['id']}_{data.get('version','1.0.0')}.zip"
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
                for p in workspace.rglob("*"):
                    if p.is_file() and release_dir not in p.parents:
                        z.write(p, p.relative_to(workspace))
            checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
            manifest = release_dir / "manifest.json"
            manifest.write_text(json.dumps({
                "specification_id": data["id"],
                "module_name": module_name,
                "template_id": template.template_id,
                "certified": True,
                "tests_passed": test_result.passed,
                "time_reduction": productivity.reduction_ratio,
                "meets_45_percent_target": productivity.meets_45_percent_target,
                "archive": archive.name,
                "sha256": checksum,
            }, indent=2), encoding="utf-8")

            tx.commit()
            return {
                "module_name": module_name,
                "artifacts": len(generated.artifacts) + 4,
                "tests_passed": test_result.passed,
                "certified": cert.certified,
                "time_reduction": productivity.reduction_ratio,
                "meets_45_percent_target": productivity.meets_45_percent_target,
                "archive": str(archive),
                "manifest": str(manifest),
                "sha256": checksum,
            }
        except Exception:
            tx.rollback()
            raise
