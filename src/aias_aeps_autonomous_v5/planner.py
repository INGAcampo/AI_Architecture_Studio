"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations
from .models import PipelinePlan

class PipelinePlanner:
    """Execute the public PipelinePlanner operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    DEFAULT_STAGES = [
        "load_specification",
        "select_assets",
        "compile",
        "generate_code",
        "generate_tests",
        "generate_docs",
        "validate",
        "certify",
        "package",
    ]

    def plan(self, specification: dict) -> PipelinePlan:
        """Execute the public PipelinePlanner.plan operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        stages = list(self.DEFAULT_STAGES)
        if specification.get("skip_docs"):
            stages.remove("generate_docs")
        parallel = [["generate_code", "generate_tests", "generate_docs"]]
        return PipelinePlan(
            plan_id=f"PLAN-{specification['id'].split('-')[-1]}",
            stages=stages,
            parallel_groups=parallel,
            metadata={"domain": specification.get("domain", "generic")},
        )
