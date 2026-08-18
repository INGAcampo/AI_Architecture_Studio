"""Hash-chained external evidence ledger for EXTERNAL-GATES-001."""
from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import datetime
import hashlib,json
from pathlib import Path

ALLOWED_GATES={"EXT-NORMATIVE","EXT-BENCHMARK","EXT-VENDOR","EXT-MATURITY"}
@dataclass(frozen=True,slots=True)
class ExternalEvidenceRecord:
 record_id:str;gate_id:str;evidence_type:str;issuer:str;issued_at:str;artifact_locator:str;artifact_sha256:str;authority_verification_reference:str;previous_hash:str;record_hash:str
class ExternalEvidenceLedger:
 @staticmethod
 def _hash(payload):return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
 def load(self,path:Path):
  if not path.exists():return []
  return json.loads(path.read_text(encoding="utf-8")).get("records",[])
 def validate(self,records):
  issues=[];previous="GENESIS";ids=[]
  for index,row in enumerate(records):
   ids.append(row.get("record_id"));body={k:v for k,v in row.items() if k!="record_hash"}
   if row.get("gate_id") not in ALLOWED_GATES:issues.append(f"{index}:unsupported_gate")
   if row.get("previous_hash")!=previous:issues.append(f"{index}:chain_break")
   if len(row.get("artifact_sha256",""))!=64:issues.append(f"{index}:artifact_hash_invalid")
   if not all(row.get(x) for x in ("record_id","evidence_type","issuer","issued_at","artifact_locator","authority_verification_reference")):issues.append(f"{index}:evidence_incomplete")
   calculated=self._hash(body)
   if row.get("record_hash")!=calculated:issues.append(f"{index}:record_hash_invalid")
   previous=row.get("record_hash","")
  if len(ids)!=len(set(ids)):issues.append("duplicate_record_id")
  return issues
 def append(self,path:Path,record_id,gate_id,evidence_type,issuer,issued_at,artifact_locator,artifact_sha256,authority_verification_reference):
  records=self.load(path);issues=self.validate(records)
  if issues:raise ValueError(f"existing_ledger_invalid:{issues}")
  if gate_id not in ALLOWED_GATES:raise ValueError("unsupported_gate")
  try:datetime.fromisoformat(issued_at.replace("Z","+00:00"))
  except ValueError as exc:raise ValueError("issued_at_invalid") from exc
  if len(artifact_sha256)!=64 or not authority_verification_reference:raise ValueError("external_evidence_incomplete")
  body={"record_id":record_id,"gate_id":gate_id,"evidence_type":evidence_type,"issuer":issuer,"issued_at":issued_at,"artifact_locator":artifact_locator,"artifact_sha256":artifact_sha256,"authority_verification_reference":authority_verification_reference,"previous_hash":records[-1]["record_hash"] if records else "GENESIS"};body["record_hash"]=self._hash(body)
  records.append(body);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps({"ledger_id":"EXTERNAL-EVIDENCE-LEDGER-001","records":records},ensure_ascii=False,indent=2)+"\n",encoding="utf-8");return ExternalEvidenceRecord(**body)
