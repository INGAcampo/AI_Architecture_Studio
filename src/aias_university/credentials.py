"""HMAC-verifiable internal competency credentials with explicit legal limitations."""
from __future__ import annotations
import hashlib,hmac,json
from datetime import datetime,timezone
class CredentialIssuer:
 """Issue and verify tamper-evident AIAS internal credentials for eligible learners."""
 def __init__(self,issuer_id:str,secret:bytes):
  if len(secret)<32:raise ValueError("credential_secret_too_short")
  self.issuer_id=issuer_id;self.secret=secret
 def issue(self,engine,learner_id:str,course_id:str,identity_verified:bool)->dict:
  """Issue an internal competency only after eligibility and identity verification."""
  if not identity_verified:raise PermissionError("identity_verification_required")
  if not engine.eligible(learner_id,course_id):raise PermissionError("learner_not_eligible")
  course=engine.catalog.get(course_id);payload={"credential_id":f"CRED-{hashlib.sha256(f'{learner_id}|{course_id}'.encode()).hexdigest()[:16].upper()}","type":"AIAS_INTERNAL_COMPETENCY","learner_id":learner_id,"course_id":course_id,"course_version":course["version"],"issuer":self.issuer_id,"issued_at":datetime.now(timezone.utc).isoformat(),"not_a_professional_license":True};payload["signature"]=self._sign(payload);return payload
 def verify(self,credential:dict)->bool:
  """Verify credential integrity using constant-time HMAC comparison."""
  signature=credential.get("signature","");payload={k:v for k,v in credential.items() if k!="signature"};return hmac.compare_digest(signature,self._sign(payload))
 def _sign(self,payload:dict)->str:
  return hmac.new(self.secret,json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode(),hashlib.sha256).hexdigest()
