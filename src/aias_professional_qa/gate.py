from __future__ import annotations
import hashlib,json
class ProfessionalQAGate:
    """Independent executive-readiness verdict; score never overrides blockers."""
    def evaluate(self, artifacts):
        matrix=[]
        for name,status,evidence,dependency,action in artifacts:
            matrix.append({"output":name,"status":status,"evidence_sha256":hashlib.sha256(str(evidence).encode()).hexdigest(),"dependency":dependency,"action_to_elevate":action})
        blocked=[x for x in matrix if x['status']=='BLOCKED']; preliminary=[x for x in matrix if x['status']=='PRELIMINARY']; limited=[x for x in matrix if x['status']=='V0_LIMITED']
        findings=[]
        for x in blocked: findings.append({"severity":"CRITICAL","output":x['output'],"message":x['action_to_elevate']})
        for x in preliminary+limited: findings.append({"severity":"MAJOR","output":x['output'],"message":x['action_to_elevate']})
        score=round(100*(len(matrix)-len(blocked)*2-len(preliminary)-len(limited))/max(1,len(matrix)),2)
        verdict='NOT_READY' if blocked else ('CONDITIONALLY_READY' if preliminary or limited else 'READY_FOR_EXECUTIVE_REISSUANCE')
        return {"verdict":verdict,"score":max(0,score),"matrix":matrix,"findings":findings,"hash":hashlib.sha256(json.dumps(matrix,sort_keys=True).encode()).hexdigest()}
