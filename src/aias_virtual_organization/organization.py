"""Persistent assignment, segregation of duties and professional escalation."""
from __future__ import annotations
import json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path
from .models import VirtualEngineer,WorkOrder

class VirtualEngineeringOrganization:
    """Route work to qualified virtual engineers without exceeding authority."""
    def __init__(self,path:Path):self.path=path;self.data=self._load()
    def _load(self):return json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {"schema_version":"1.0.0","engineers":{},"work":{}}
    def register(self,engineer:VirtualEngineer)->dict:
        """Register a virtual engineer idempotently and reject identity drift."""
        engineer.validate();row=engineer.to_dict();old=self.data["engineers"].get(engineer.engineer_id)
        if old and old!=row:raise ValueError("virtual_engineer_conflict")
        self.data["engineers"][engineer.engineer_id]=row;self._save();return row
    def assign(self,order:WorkOrder,exclude:set[str]|None=None)->dict:
        """Assign the least-loaded available engineer with complete competency and action authority."""
        order.validate();exclude=exclude or set();required=set(order.required_competencies);loads={eid:sum(w.get("assignee")==eid and w["status"] not in {"COMPLETED","REJECTED"} for w in self.data["work"].values()) for eid in self.data["engineers"]}
        candidates=[e for e in self.data["engineers"].values() if e["engineer_id"] not in exclude and e["status"]=="AVAILABLE" and required<=set(e["competencies"]) and order.action in e["authorized_actions"]]
        if not candidates:raise ValueError("no_authorized_virtual_engineer")
        selected=sorted(candidates,key=lambda e:(loads[e["engineer_id"]],e["engineer_id"]))[0];row={"work_id":order.work_id,"title":order.title,"action":order.action,"source_ref":order.source_ref,"risk_level":order.risk_level,"regulated":order.regulated,"assignee":selected["engineer_id"],"status":"ASSIGNED","assigned_at":datetime.now(timezone.utc).isoformat(),"metadata":order.metadata,"history":[]};self.data["work"][order.work_id]=row;self._save();return row
    def submit(self,work_id:str,evidence:dict)->dict:
        """Submit work only with implementation evidence and mark regulated output for human approval."""
        row=self._work(work_id)
        if row["status"]!="ASSIGNED" or not evidence.get("artifact") or not evidence.get("validation"):raise ValueError("incomplete_work_submission")
        row.update({"status":"SUBMITTED","evidence":evidence,"submitted_at":datetime.now(timezone.utc).isoformat(),"human_professional_approval_required":row["regulated"] or row["risk_level"] in {"HIGH","CRITICAL"}});self._save();return row
    def assign_review(self,work_id:str,review_competency:str)->dict:
        """Assign an independent checker by excluding the producing engineer."""
        source=self._work(work_id)
        if source["status"]!="SUBMITTED":raise ValueError("work_not_submitted")
        review=WorkOrder(f"REVIEW-{work_id}",f"Review {source['title']}",(review_competency,),"review",source["source_ref"],source["risk_level"],source["regulated"],{"source_work_id":work_id});row=self.assign(review,{source["assignee"]});source["review_work_id"]=row["work_id"];self._save();return row
    def complete_review(self,review_work_id:str,decision:str,evidence:dict)->dict:
        """Record independent review while reserving regulated approval for a human professional."""
        review=self._work(review_work_id)
        if review["status"]!="ASSIGNED" or decision not in {"ACCEPT","REJECT"} or not evidence.get("review_report"):raise ValueError("invalid_review_completion")
        source=self._work(review["metadata"]["source_work_id"]);review.update({"status":"COMPLETED","decision":decision,"evidence":evidence});source["status"]="REVIEWED" if decision=="ACCEPT" else "REJECTED";source["virtual_review_accepted"]=decision=="ACCEPT";source["final_authority"]="HUMAN_LICENSED_PROFESSIONAL" if source["human_professional_approval_required"] else "GOVERNED_WORKFLOW";self._save();return source
    def _work(self,work_id):
        if work_id not in self.data["work"]:raise ValueError("unknown_work_order")
        return self.data["work"][work_id]
    def _save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True);fd,name=tempfile.mkstemp(dir=self.path.parent,suffix=".tmp")
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as stream:json.dump(self.data,stream,ensure_ascii=False,indent=2,sort_keys=True);stream.write("\n")
            os.replace(name,self.path)
        finally:
            if os.path.exists(name):os.unlink(name)
