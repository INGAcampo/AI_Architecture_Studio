"""Executable readiness model for external conditions AIAS cannot self-issue."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import hashlib,json
from pathlib import Path

@dataclass(frozen=True,slots=True)
class ExternalGate:
 gate_id:str;name:str;authority:str;owner_role:str;required_evidence:tuple[str,...];next_action:str;status:str="WAITING_EXTERNAL_AUTHORITY"
@dataclass(frozen=True,slots=True)
class ExternalGatePortfolio:
 portfolio_id:str;gates:tuple[ExternalGate,...];status:str;sha256:str

def default_gates():
 return (
  ExternalGate("EXT-NORMATIVE","Licensed jurisdictional standards","Authorized publishers and project jurisdiction","Project Director / Legal",("purchase authorization","license record","applicable jurisdiction decision","version record"),"Approve jurisdiction, budget and licensed acquisition"),
  ExternalGate("EXT-BENCHMARK","Independent benchmark acceptance","Qualified independent engineering reviewer","Engineering Director",("independent dataset","method statement","signed review","accepted deviations"),"Appoint an independent reviewer and approve benchmark scope"),
  ExternalGate("EXT-VENDOR","Licensed engineering application runtimes","Autodesk, CSI and Autodesk Robot licensing authorities","Technology Director",("license entitlement","supported API version","test environment","vendor execution evidence"),"Approve products, versions, seats and integration environment"),
  ExternalGate("EXT-MATURITY","Longitudinal maturity evidence and audit","Real clients, jurisdictions and independent appraiser","Executive Management / Quality",("365 observation days","10 completed production projects","professional acceptance","independent conformant audit"),"Continue authenticated evidence campaign until thresholds are real"),
 )
class ExternalGateManager:
 def evaluate(self,evidence:dict[str,dict]):
  rows=[]
  for gate in default_gates():
   supplied=evidence.get(gate.gate_id,{});verified=set(supplied.get("verified_evidence",()))
   complete=set(gate.required_evidence)<=verified and supplied.get("authority_verified") is True
   rows.append(ExternalGate(gate.gate_id,gate.name,gate.authority,gate.owner_role,gate.required_evidence,gate.next_action,"SATISFIED" if complete else "WAITING_EXTERNAL_AUTHORITY"))
  status="ALL_EXTERNAL_GATES_SATISFIED" if all(x.status=="SATISFIED" for x in rows) else "WAITING_EXTERNAL_AUTHORITIES"
  payload={"portfolio_id":"EXTERNAL-GATES-001","gates":[asdict(x) for x in rows],"status":status};digest=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
  return ExternalGatePortfolio("EXTERNAL-GATES-001",tuple(rows),status,digest)
 def evaluate_ledger(self,records:list[dict],authority_registry:dict[str,str]):
  from .evidence import ExternalEvidenceLedger
  issues=ExternalEvidenceLedger().validate(records)
  if issues:raise ValueError(f"external_evidence_ledger_invalid:{issues}")
  evidence={}
  for row in records:
   prefix=authority_registry.get(row["issuer"]);trusted=bool(prefix and row["authority_verification_reference"].startswith(prefix))
   gate=evidence.setdefault(row["gate_id"],{"verified_evidence":[],"authority_verified":True})
   if trusted:gate["verified_evidence"].append(row["evidence_type"])
   else:gate["authority_verified"]=False
  return self.evaluate(evidence)
 def write(self,evidence:dict[str,dict],output:Path):
  portfolio=self.evaluate(evidence);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(asdict(portfolio),ensure_ascii=False,indent=2)+"\n",encoding="utf-8");return portfolio
