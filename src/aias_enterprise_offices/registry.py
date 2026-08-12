"""Office authority registry with deterministic intake and audit evidence."""
from __future__ import annotations
import json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path
from .models import OfficeCharter,WorkItem

class OfficeRegistry:
    """Persist approved charters and route work without ambiguous ownership."""
    def __init__(self,path:Path):self.path=path;self.data=self._load()
    def _load(self):return json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {"schema_version":"1.0.0","offices":{},"work_items":{}}
    def register(self,charter:OfficeCharter)->dict:
        """Register an approved office charter idempotently and reject conflicts."""
        charter.validate();row=charter.to_dict();old=self.data["offices"].get(charter.office_id)
        if old and old!=row:raise ValueError("office_charter_conflict")
        self.data["offices"][charter.office_id]=row;self._save();return row
    def dependency_readiness(self,charter:OfficeCharter,operational_concepts:set[str])->dict:
        """Report whether every declared institutional dependency is operational."""
        missing=sorted(set(charter.dependencies)-operational_concepts);return {"ready":not missing,"missing":missing}
    def route(self,item:WorkItem)->dict:
        """Assign a unique accountable office by declared accountability category."""
        if not item.item_id or not item.category or not item.source:raise ValueError("invalid_work_item")
        candidates=[office for office in self.data["offices"].values() if item.category in office["accountable_for"]]
        if len(candidates)!=1:raise ValueError("ambiguous_or_missing_accountability")
        row={"item_id":item.item_id,"category":item.category,"title":item.title,"source":item.source,"office_id":candidates[0]["office_id"],"status":"ASSIGNED","assigned_at":datetime.now(timezone.utc).isoformat(),"evidence":item.evidence};self.data["work_items"][item.item_id]=row;self._save();return row
    def decide(self,item_id:str,decision:str,evidence:dict,actor_role:str)->dict:
        """Record a decision only for a charter-authorized role with required evidence."""
        row=self.data["work_items"].get(item_id)
        if not row:raise ValueError("unknown_work_item")
        charter=self.data["offices"][row["office_id"]]
        if actor_role not in charter["decision_rights"]:raise ValueError("unauthorized_office_decision")
        missing=[key for key in charter["required_evidence"] if key not in evidence]
        if missing:raise ValueError("missing_decision_evidence:"+",".join(missing))
        row.update({"status":"DECIDED","decision":decision,"decision_evidence":evidence,"decided_at":datetime.now(timezone.utc).isoformat()});self._save();return row
    def _save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True);fd,name=tempfile.mkstemp(dir=self.path.parent,suffix=".tmp")
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as stream:json.dump(self.data,stream,ensure_ascii=False,indent=2,sort_keys=True);stream.write("\n")
            os.replace(name,self.path)
        finally:
            if os.path.exists(name):os.unlink(name)
