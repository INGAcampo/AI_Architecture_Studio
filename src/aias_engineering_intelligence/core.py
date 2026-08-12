"""Evidence-only recommendation, abstention and auditable reasoning records."""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from .models import Evidence,IntelligenceRequest,Recommendation
from .policy import IntelligencePolicy
class EngineeringIntelligenceCore:
    """Issue bounded recommendations only when policy evidence gates are met."""
    def __init__(self,policy:IntelligencePolicy|None=None):self.policy=policy or IntelligencePolicy();self.audit=[]
    def recommend(self,request:IntelligenceRequest,evidence:list[Evidence],candidate_action:str)->Recommendation:
        """Recommend an explicit candidate action or abstain with concrete reasons."""
        assessment=self.policy.assess(request,evidence);reasons=[]
        if assessment["missing"]:reasons.append("missing_claims:"+",".join(assessment["missing"]))
        if assessment["conflicts"]:reasons.append("conflicting_claims:"+",".join(assessment["conflicts"]))
        if assessment["confidence"]<assessment["threshold"]:reasons.append(f"confidence_below_threshold:{assessment['confidence']:.4f}<{assessment['threshold']:.4f}")
        status="ABSTAIN" if reasons else "RECOMMEND";text="No recommendation; additional verified evidence or conflict resolution required." if reasons else candidate_action;professional=request.regulated or request.risk_level in {"HIGH","CRITICAL"};result=Recommendation(request.request_id,status,text,assessment["confidence"],tuple(sorted(x.evidence_id for x in evidence)),tuple(reasons),professional,"HUMAN_LICENSED_PROFESSIONAL" if professional else "GOVERNED_WORKFLOW");self._record(request,result,assessment);return result
    def _record(self,request,result,assessment):
        row={"request_id":request.request_id,"context_ref":request.context_ref,"result":result.to_dict(),"assessment":assessment,"recorded_at":datetime.now(timezone.utc).isoformat()};row["record_sha256"]=hashlib.sha256(json.dumps(row,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest();self.audit.append(row)
