"""Persistent evidence system for integrated management preparation."""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from .models import CorrectiveAction, ManagementObjective, ManagementRisk
from .registry import control_families


class IntegratedManagementSystem:
    """Manage internally verified readiness without issuing external conformity claims."""

    def __init__(self, workspace: Path):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)

    def initialize(self, organization: str = "AIAS") -> dict:
        """Create the canonical integrated-system foundation and shared control map."""
        state = {
            "system_id": "AIAS-IMS-001",
            "organization": organization,
            "status": "IMPLEMENTED_FOUNDATION_NOT_CERTIFIED",
            "scope": "AIAS digital engineering company, platform, engineering production and AI-enabled services",
            "framework_targets": ["ISO-9001", "ISO-IEC-27001", "ISO-IEC-42001", "ISO-22301"],
            "certification_claim_permitted": False,
            "control_families": list(control_families()),
            "risks": [], "objectives": [], "corrective_actions": [], "audit_program": [], "management_reviews": [],
        }
        self._write("IMS_STATE.json", state)
        return state

    def add_risk(self, risk: ManagementRisk) -> dict:
        """Register a unique owned risk and preserve its calculated severity."""
        risk.validate();state=self._state()
        if any(row["risk_id"] == risk.risk_id for row in state["risks"]):raise ValueError("duplicate_management_risk")
        row=risk.to_dict();state["risks"].append(row);self._write("IMS_STATE.json",state);return row

    def add_objective(self, objective: ManagementObjective) -> dict:
        """Register a unique measurable objective without claiming that its target is achieved."""
        objective.validate();state=self._state()
        if any(row["objective_id"] == objective.objective_id for row in state["objectives"]):raise ValueError("duplicate_management_objective")
        row=objective.to_dict();row["observed_value"]=None;row["target_achieved"]=None;state["objectives"].append(row);self._write("IMS_STATE.json",state);return row

    def add_corrective_action(self, action: CorrectiveAction) -> dict:
        """Register a unique corrective action for subsequent effectiveness review."""
        action.validate();state=self._state()
        if any(row["action_id"] == action.action_id for row in state["corrective_actions"]):raise ValueError("duplicate_corrective_action")
        row=action.to_dict();state["corrective_actions"].append(row);self._write("IMS_STATE.json",state);return row

    def schedule_internal_audit(self, audit_id: str, scope: tuple[str, ...], planned_date: str, lead: str) -> dict:
        """Schedule an internal audit while explicitly reserving certification to an external body."""
        if not audit_id.startswith("IMS-AUD-") or not scope or not lead:raise ValueError("invalid_internal_audit")
        datetime.fromisoformat(planned_date);state=self._state();row={"audit_id":audit_id,"scope":list(scope),"planned_date":planned_date,"lead":lead,"classification":"INTERNAL_AUDIT_NOT_CERTIFICATION","status":"PLANNED"};state["audit_program"].append(row);self._write("IMS_STATE.json",state);return row

    def record_management_review(self, review_id: str, inputs: dict, decisions: tuple[str, ...], reviewed_at: str) -> dict:
        """Record leadership review inputs and decisions with immutable evidence digest."""
        if not review_id.startswith("IMS-MR-") or not inputs or not decisions:raise ValueError("invalid_management_review")
        datetime.fromisoformat(reviewed_at);row={"review_id":review_id,"inputs":inputs,"decisions":list(decisions),"reviewed_at":reviewed_at};row["evidence_sha256"]=hashlib.sha256(json.dumps(row,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest();state=self._state();state["management_reviews"].append(row);self._write("IMS_STATE.json",state);return row

    def readiness(self) -> dict:
        """Report implementation evidence and explicit certification gaps."""
        state=self._state();families={row["id"] for row in state["control_families"]};required={row["id"] for row in control_families()};gaps=[]
        if families != required:gaps.append("shared_control_families_incomplete")
        if not state["risks"]:gaps.append("risk_register_empty")
        if not state["objectives"]:gaps.append("management_objectives_empty")
        if not state["audit_program"]:gaps.append("internal_audit_not_scheduled")
        if not state["management_reviews"]:gaps.append("management_review_missing")
        return {"system_id":state["system_id"],"foundation_implemented":not any(x=="shared_control_families_incomplete" for x in gaps),"internal_readiness_complete":not gaps,"externally_certified":False,"certification_claim_permitted":False,"gaps":gaps}

    def _state(self) -> dict:
        """Load current system state or initialize it on first use."""
        path=self.workspace/"IMS_STATE.json";return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else self.initialize()

    def _write(self, name: str, value: dict) -> None:
        """Persist canonical JSON evidence atomically within the IMS workspace."""
        path=self.workspace/name;temporary=path.with_suffix(path.suffix+".tmp");temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");temporary.replace(path)
