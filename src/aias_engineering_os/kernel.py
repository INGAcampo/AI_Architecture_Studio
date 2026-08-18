"""Atomic evidence-gated project lifecycle and CNS-compatible operating events."""
from __future__ import annotations
import hashlib,json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path
from .models import OperatingCommand
from .registry import ServiceRegistry
class EngineeringOperatingSystem:
    """Coordinate project state without duplicating domain-system execution."""
    STATES=("INITIATED","PLANNED","ASSIGNED","PRODUCED","REVIEWED","RELEASED","OPERATING")
    GATES={"PLANNED":("portfolio_plan",),"ASSIGNED":("work_assignment",),"PRODUCED":("production_result","validation"),"REVIEWED":("independent_review",),"RELEASED":("release","checksum"),"OPERATING":("handover","monitoring_plan")}
    def __init__(self,path:Path,services:ServiceRegistry,event_sink=None):self.path=path;self.services=services;self.event_sink=event_sink or (lambda event:None);self.data=self._load()
    def _load(self):return json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {"schema_version":"1.0.0","projects":{},"commands":{}}
    def initiate(self,project_id:str,title:str,command_id:str,correlation_id:str)->dict:
        """Create a uniquely identified project and publish its initiation event."""
        if command_id in self.data["commands"]:return self.data["commands"][command_id]
        if project_id in self.data["projects"]:raise ValueError("duplicate_project")
        row={"project_id":project_id,"title":title,"state":"INITIATED","evidence":{},"history":[self._event("INITIATED","AEOS",correlation_id,{})]};self.data["projects"][project_id]=row;result={"project_id":project_id,"state":"INITIATED","idempotent_replay":False};self.data["commands"][command_id]=result;self._save();self.event_sink({"type":"aeos.project.initiated","project_id":project_id,"correlation_id":correlation_id});return result
    def transition(self,command:OperatingCommand,required_services:tuple[str,...])->dict:
        """Advance exactly one lifecycle state after service and evidence gates pass."""
        command.validate()
        if command.command_id in self.data["commands"]:return {**self.data["commands"][command.command_id],"idempotent_replay":True}
        project=self._project(command.project_id);current=self.STATES.index(project["state"])
        if command.target_state not in self.STATES or self.STATES.index(command.target_state)!=current+1:raise ValueError("invalid_operating_transition")
        service_issues=[]
        for sid in required_services:
            ready=self.services.readiness(sid)
            if not ready["ready"]:service_issues.extend(ready["issues"])
        if service_issues:raise ValueError("services_not_ready:"+",".join(service_issues))
        missing=[key for key in self.GATES[command.target_state] if not command.evidence.get(key)]
        if missing:raise ValueError("missing_operating_evidence:"+",".join(missing))
        previous=project["state"];project["state"]=command.target_state;project["evidence"].update(command.evidence);event=self._event(command.target_state,command.actor,command.correlation_id,command.evidence);project["history"].append(event);result={"project_id":command.project_id,"previous_state":previous,"state":command.target_state,"record_sha256":event["record_sha256"],"idempotent_replay":False};self.data["commands"][command.command_id]=result;self._save();self.event_sink({"type":"aeos.project.transitioned","project_id":command.project_id,"previous_state":previous,"state":command.target_state,"correlation_id":command.correlation_id,"record_sha256":event["record_sha256"]});return result
    def status(self,project_id):
        """Return the complete current lifecycle record for operational projection."""
        return json.loads(json.dumps(self._project(project_id)))
    def _project(self,project_id):
        if project_id not in self.data["projects"]:raise ValueError("unknown_project")
        return self.data["projects"][project_id]
    def _event(self,state,actor,correlation,evidence):
        row={"state":state,"actor":actor,"correlation_id":correlation,"evidence_keys":sorted(evidence),"occurred_at":datetime.now(timezone.utc).isoformat()};row["record_sha256"]=hashlib.sha256(json.dumps(row,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest();return row
    def _save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True);fd,name=tempfile.mkstemp(dir=self.path.parent,suffix=".tmp")
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as stream:json.dump(self.data,stream,ensure_ascii=False,indent=2,sort_keys=True);stream.write("\n")
            os.replace(name,self.path)
        finally:
            if os.path.exists(name):os.unlink(name)
