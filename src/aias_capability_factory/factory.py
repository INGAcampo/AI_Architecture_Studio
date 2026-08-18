"""Blueprint compiler and end-to-end governed capability materialization."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
from aias_development_platform import DevelopmentJob,DevelopmentPlatform
from .models import CapabilityBlueprint
from .registry import CapabilityRegistry
from .vertical import CompleteVerticalGate

class CapabilityFactory:
    """Compile approved blueprints and drive them through certified production."""
    def __init__(self,registry:CapabilityRegistry,platform:DevelopmentPlatform,production_root:Path,event_sink=None,vertical_gate=None):self.registry=registry;self.platform=platform;self.production_root=production_root;self.event_sink=event_sink or (lambda event:None);self.vertical_gate=vertical_gate or CompleteVerticalGate()
    def materialize(self,blueprint:CapabilityBlueprint)->dict:
        """Produce, validate and release one capability while retaining every gate."""
        vertical=self.vertical_gate.require(blueprint.metadata.get("vertical_evidence",{}),user_facing=bool(blueprint.metadata.get("user_facing",False)),regulated=bool(blueprint.metadata.get("regulated",False)))
        self.registry.register(blueprint);self.registry.advance(blueprint.capability_id,"APPROVED",{"approval_id":blueprint.approval_id})
        slug=re.sub(r"[^a-z0-9_]+","_",blueprint.name.lower()).strip("_");workspace=(self.production_root/blueprint.capability_id).resolve();workspace.mkdir(parents=True,exist_ok=True);spec=workspace/"capability_spec.json"
        payload={"id":self._spec_id(blueprint.capability_id),"title":blueprint.name,"module_name":slug,"version":blueprint.version,"domain":blueprint.domain,"requirements":list(blueprint.requirements),"dependencies":[],"architecture_refs":list(blueprint.architecture_refs),"adr_refs":list(blueprint.adr_refs),**blueprint.metadata}
        spec.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");result=self.platform.execute(DevelopmentJob(f"JOB-{blueprint.capability_id}",spec,workspace/"build",blueprint.engine_mode,f"COR-{blueprint.capability_id}"))
        dev={"engine":result.engine,"certified":result.certified,"artifacts":list(result.artifacts),"evidence":result.evidence};self.registry.advance(blueprint.capability_id,"MATERIALIZED",{"development_result":dev})
        if not result.certified:raise RuntimeError("capability_not_certified")
        validation={"certified":True,"requirements":len(blueprint.requirements),"traceability":1.0,"professional_review_required":True,"complete_vertical_gate":vertical.to_dict()};self.registry.advance(blueprint.capability_id,"VALIDATED",{"validation":validation})
        release=self._release_evidence(result);record=self.registry.advance(blueprint.capability_id,"RELEASED",{"release":release});self.event_sink({"type":"capability.released","capability_id":blueprint.capability_id,"version":blueprint.version,"sha256":release["sha256"]});return record
    def _spec_id(self,capability_id):
        digits="".join(c for c in capability_id if c.isdigit());return f"SPEC-{(digits or '1')[-6:].zfill(6)}"
    def _release_evidence(self,result):
        archive=result.evidence.get("release",{}).get("archive") or result.evidence.get("archive") or next((x for x in result.artifacts if str(x).endswith(".zip")),None)
        if not archive:raise ValueError("missing_release_archive")
        path=Path(archive);digest=result.evidence.get("release",{}).get("sha256") or result.evidence.get("sha256") or hashlib.sha256(path.read_bytes()).hexdigest();return {"archive":str(path),"sha256":digest}
