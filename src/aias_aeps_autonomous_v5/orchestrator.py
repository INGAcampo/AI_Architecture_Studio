"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations
from pathlib import Path
import json, hashlib, zipfile
from .catalog import PersistentAssetCatalog
from .models import AssetRecord, BuildResult
from .selection import IntelligentTemplateSelector
from .planner import PipelinePlanner
from .cache import CompilationCache
from .security import SecurityPolicyEngine
from .observability import Observability
from .incremental import IncrementalExecutionEngine
from .parallel import ParallelExecutionEngine
from .generation import MultiDomainProgramGenerator
from .execution import WorkspaceTestRunner
from .certification import AutonomousCertificationEngine

class AutonomousEngineeringOrchestrator:
    """Execute the public AutonomousEngineeringOrchestrator operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    def build(self, spec_file: Path, workspace: Path) -> BuildResult:
        """Build the build required by autonomous engineering planning and controlled execution from explicit inputs."""
        specification = json.loads(spec_file.read_text(encoding="utf-8"))
        workspace.mkdir(parents=True, exist_ok=True)
        obs = Observability()
        obs.emit("build.started", specification_id=specification["id"])

        catalog = PersistentAssetCatalog(workspace / ".aeps" / "catalog.json")
        if not catalog.assets:
            catalog.add(AssetRecord("TPL-100001","template","BIM","1.0.0",{"capabilities":["modeling"],"priority":10}))
            catalog.add(AssetRecord("TPL-100002","template","Structural","1.0.0",{"capabilities":["analysis"],"priority":10}))
            catalog.add(AssetRecord("TPL-100003","template","generic","1.0.0",{"capabilities":[],"priority":1}))
            catalog.save()

        templates = [
            {
                "template_id": a.asset_id,
                "domain": a.domain,
                "capabilities": a.payload.get("capabilities", []),
                "priority": a.payload.get("priority", 0),
            }
            for a in catalog.assets.values()
            if a.asset_type == "template"
        ]
        selected = IntelligentTemplateSelector().select(specification, templates)
        plan = PipelinePlanner().plan(specification)

        cache = CompilationCache(workspace / ".aeps" / "cache")
        key = cache.key_for(specification)
        if cache.has(key):
            cached = cache.get(key)
            obs.emit("cache.hit", key=key)
            return BuildResult(
                certified=cached["certified"],
                cache_hit=True,
                artifacts=[Path(p) for p in cached["artifacts"]],
                reports={**cached["reports"], "events": obs.events, "metrics": obs.metrics},
            )

        security = SecurityPolicyEngine()
        security_issues = security.scan_specification(specification)

        generator = MultiDomainProgramGenerator()
        jobs = {
            "generate": lambda: generator.generate(specification, workspace),
            "plan": lambda: {
                "plan_id": plan.plan_id,
                "stages": plan.stages,
                "parallel_groups": plan.parallel_groups,
            },
        }
        parallel_results = ParallelExecutionEngine().run(jobs)
        artifacts = parallel_results["generate"]
        test_report = WorkspaceTestRunner().run(workspace)
        security_issues += security.scan_workspace(workspace)

        certification = AutonomousCertificationEngine().certify(
            specification, test_report, security_issues, workspace
        )
        if not certification["certified"]:
            raise RuntimeError(f"Certification failed: {certification['issues']}")

        release = workspace / "release"
        release.mkdir(parents=True, exist_ok=True)
        archive = release / f"{specification['id']}_{specification['version']}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for path in workspace.rglob("*"):
                if path.is_file() and release not in path.parents:
                    z.write(path, path.relative_to(workspace))
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()

        reports = {
            "selected_template": selected,
            "plan": parallel_results["plan"],
            "test_report": test_report,
            "certification": certification,
            "archive": str(archive),
            "sha256": digest,
            "events": obs.events,
            "metrics": obs.metrics,
            "incremental_stages": IncrementalExecutionEngine().changed_stages(None, specification),
        }
        payload = {
            "certified": True,
            "artifacts": [str(p) for p in artifacts] + [str(archive)],
            "reports": reports,
        }
        cache.put(key, payload)
        obs.emit("build.completed", certified=True)
        return BuildResult(True, False, artifacts + [archive], {**reports, "events": obs.events})
