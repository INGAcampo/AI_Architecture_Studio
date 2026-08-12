"""Atomic capability registry with strict lifecycle transitions."""
from __future__ import annotations
import json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path
from .models import CapabilityBlueprint

class CapabilityRegistry:
    """Persist unique blueprints and sequential evidence-gated lifecycle states."""
    STATES=("DRAFT","APPROVED","MATERIALIZED","VALIDATED","RELEASED")
    REQUIRED={"APPROVED":"approval_id","MATERIALIZED":"development_result","VALIDATED":"validation","RELEASED":"release"}
    def __init__(self,path:Path):self.path=path;self.data=self._load()
    def _load(self):return json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {"schema_version":"1.0.0","capabilities":{}}
    def register(self,blueprint:CapabilityBlueprint)->dict:
        """Register an immutable blueprint once in DRAFT state."""
        blueprint.validate();row=self.data["capabilities"].get(blueprint.capability_id);payload=blueprint.to_dict()
        if row and row["blueprint"]!=payload:raise ValueError("capability_id_conflict")
        if not row:self.data["capabilities"][blueprint.capability_id]={"capability_id":blueprint.capability_id,"state":"DRAFT","version":blueprint.version,"blueprint":payload,"evidence":{},"history":[self._event("DRAFT",{})]};self._save()
        return self.data["capabilities"][blueprint.capability_id]
    def advance(self,capability_id:str,target:str,evidence:dict)->dict:
        """Advance exactly one state only when target-specific evidence exists."""
        row=self.data["capabilities"].get(capability_id)
        if not row:raise ValueError("unknown_capability")
        current=self.STATES.index(row["state"])
        if target not in self.STATES or self.STATES.index(target)!=current+1:raise ValueError("invalid_lifecycle_transition")
        required=self.REQUIRED[target]
        if not evidence.get(required):raise ValueError(f"missing_gate_evidence:{required}")
        row["state"]=target;row["evidence"].update(evidence);row["history"].append(self._event(target,evidence));self._save();return row
    def _event(self,state,evidence):return {"state":state,"occurred_at":datetime.now(timezone.utc).isoformat(),"evidence_keys":sorted(evidence)}
    def _save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True);fd,name=tempfile.mkstemp(dir=self.path.parent,suffix=".tmp")
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as stream:json.dump(self.data,stream,ensure_ascii=False,indent=2,sort_keys=True);stream.write("\n")
            os.replace(name,self.path)
        finally:
            if os.path.exists(name):os.unlink(name)
