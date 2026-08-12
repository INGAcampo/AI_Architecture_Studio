"""Public module supporting the executable AIAS engineering operating system."""
from __future__ import annotations
import json
from pathlib import Path

class EngineeringSystemValidator:
    """Execute the public EngineeringSystemValidator operation for the executable AIAS engineering operating system using explicit caller inputs."""
    REQUIRED_EVIDENCE = {"specification","architecture","adr","traceability","tests","quality_gates","documentation","installer","release","operational_feedback"}
    def validate(self, system_path: Path, registry_path: Path) -> dict:
        """Validate validate for the executable AIAS engineering operating system and report explicit issues."""
        system=json.loads(system_path.read_text(encoding="utf-8"));registry=json.loads(registry_path.read_text(encoding="utf-8"));issues=[]
        lifecycle=system.get("asset_lifecycle",[])
        if len(lifecycle)!=len(set(lifecycle)) or lifecycle[0]!="PROPOSED" or lifecycle[-1]!="RETIRED": issues.append("invalid asset lifecycle")
        if set(system.get("mandatory_evidence",[])) != self.REQUIRED_EVIDENCE: issues.append("mandatory evidence mismatch")
        owners={office["id"] for office in system.get("offices",[])};ids=set();required=set(registry.get("required_fields",[]))
        for standard in registry.get("standards",[]):
            missing=required-set(standard)
            if missing: issues.append(f"{standard.get('id','UNKNOWN')}: missing {sorted(missing)}")
            if standard.get("id") in ids: issues.append(f"duplicate standard {standard.get('id')}")
            ids.add(standard.get("id"))
            if standard.get("owner") not in owners: issues.append(f"{standard.get('id')}: unknown owner")
            if standard.get("status") not in registry.get("allowed_statuses",[]): issues.append(f"{standard.get('id')}: invalid status")
            if not standard.get("normative_rules") or not standard.get("verification"): issues.append(f"{standard.get('id')}: unverifiable")
        return {"valid":not issues,"issues":issues,"standards":len(ids),"offices":len(owners),"lifecycle_states":len(lifecycle)}
