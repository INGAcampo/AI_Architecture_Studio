"""Selection and safety policy for governed AIAS development jobs."""
from __future__ import annotations
import json
from pathlib import Path
from .contracts import DevelopmentJob


class DevelopmentPolicy:
    """Validate job boundaries and choose the least complex capable engine."""
    ENGINES=("v3","v4","v5")
    def validate(self, job: DevelopmentJob, allowed_root: Path) -> dict:
        """Reject missing specifications, unsafe workspaces and unsupported modes."""
        if not job.job_id or not job.correlation_id: raise ValueError("missing_job_identity")
        if job.mode not in ("auto",)+self.ENGINES: raise ValueError("unsupported_engine_mode")
        specification=job.specification.resolve();workspace=job.workspace.resolve();root=allowed_root.resolve()
        if not specification.is_file(): raise ValueError("specification_not_found")
        if workspace == root or root not in workspace.parents: raise ValueError("workspace_outside_allowed_root")
        payload=json.loads(specification.read_text(encoding="utf-8"))
        required={"id","version"};missing=sorted(required-set(payload))
        if missing: raise ValueError(f"incomplete_specification:{','.join(missing)}")
        return payload
    def select(self, payload: dict, requested: str="auto") -> str:
        """Select V3, V4 or V5 from explicit mode or declared production needs."""
        if requested != "auto": return requested
        if payload.get("autonomous") or payload.get("domains") or payload.get("incremental"): return "v5"
        if payload.get("template_id") or payload.get("productivity_measurement") or payload.get("transactional"): return "v4"
        return "v3"
