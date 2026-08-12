"""Deterministic confidence, conflict and professional-authority policy."""
from __future__ import annotations
from .models import Evidence,IntelligenceRequest
class IntelligencePolicy:
    """Require evidence coverage and higher confidence as decision risk rises."""
    THRESHOLDS={"LOW":.65,"MEDIUM":.75,"HIGH":.85,"CRITICAL":.95}
    def assess(self,request:IntelligenceRequest,evidence:list[Evidence])->dict:
        """Compute coverage, trust, conflicts and the applicable decision threshold."""
        request.validate();[item.validate() for item in evidence];by_claim={claim:[] for claim in request.required_claims}
        for item in evidence:
            if item.claim in by_claim:by_claim[item.claim].append(item)
        missing=sorted(claim for claim,items in by_claim.items() if not items);conflicts=[]
        for claim,items in by_claim.items():
            values={self._stable(x.value) for x in items}
            if len(values)>1:conflicts.append(claim)
        coverage=(len(request.required_claims)-len(missing))/len(request.required_claims);trust=sum(max((x.trust for x in items),default=0) for items in by_claim.values())/len(request.required_claims);confidence=round(coverage*trust*(0 if conflicts else 1),4)
        return {"coverage":coverage,"trust":trust,"confidence":confidence,"threshold":self.THRESHOLDS[request.risk_level],"missing":missing,"conflicts":sorted(conflicts)}
    @staticmethod
    def _stable(value):
        import json
        return json.dumps(value,sort_keys=True,separators=(",",":"),default=str)
