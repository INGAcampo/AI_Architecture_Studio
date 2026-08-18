from __future__ import annotations
import hashlib,json
class ExecutiveReissuanceCampaign:
    """Fail-closed PRO-08 closure campaign; records external/evidence blockers precisely."""
    def backend_discovery(self, candidates):
        usable=[x for x in candidates if x.get('available') and x.get('native_dwg')]
        return {'status':'AVAILABLE','backend':usable[0]} if usable else {'status':'BLOCKED_BACKEND_UNAVAILABLE','backend':None}
    def xlsx_refresh(self, graph_fingerprint, prior_fingerprint):
        return {'status':'REFRESHED' if graph_fingerprint!=prior_fingerprint else 'NO_CHANGE','graph_fingerprint':graph_fingerprint,'sha256':hashlib.sha256((graph_fingerprint+'xlsx').encode()).hexdigest()}
    def manifest(self, artifacts):
        critical=[x for x in artifacts if x['status']=='BLOCKED']; verdict='NOT_READY' if critical else 'CONDITIONALLY_READY'
        return {'verdict':verdict,'critical_blockers':len(critical),'artifacts':artifacts,'sha256':hashlib.sha256(json.dumps(artifacts,sort_keys=True).encode()).hexdigest()}
