from aias_roadmap_audit import ExternalGateManager,default_gates
from aias_roadmap_audit import ExternalEvidenceLedger
def test_four_external_gates_are_actionable_and_not_self_certified():
 p=ExternalGateManager().evaluate({});assert len(p.gates)==4 and p.status=="WAITING_EXTERNAL_AUTHORITIES";assert all(x.authority and x.owner_role and x.next_action and x.required_evidence for x in p.gates);assert len(p.sha256)==64
def test_partial_internal_evidence_does_not_close_external_gate():
 g=default_gates()[0];p=ExternalGateManager().evaluate({g.gate_id:{"verified_evidence":g.required_evidence,"authority_verified":False}});assert p.gates[0].status=="WAITING_EXTERNAL_AUTHORITY"
def test_authority_verified_complete_evidence_closes_only_matching_gate():
 g=default_gates()[0];p=ExternalGateManager().evaluate({g.gate_id:{"verified_evidence":g.required_evidence,"authority_verified":True}});assert p.gates[0].status=="SATISFIED" and p.status=="WAITING_EXTERNAL_AUTHORITIES"
def test_ledger_closes_gate_only_for_registered_authority(tmp_path):
 g=default_gates()[0];path=tmp_path/"ledger.json";ledger=ExternalEvidenceLedger()
 for index,kind in enumerate(g.required_evidence):ledger.append(path,f"R{index}",g.gate_id,kind,"Publisher","2026-08-03T00:00:00Z",f"evidence://{index}","a"*64,f"https://authority.example/verify/{index}")
 p=ExternalGateManager().evaluate_ledger(ledger.load(path),{"Publisher":"https://authority.example/verify/"});assert p.gates[0].status=="SATISFIED"
 p=ExternalGateManager().evaluate_ledger(ledger.load(path),{});assert p.gates[0].status=="WAITING_EXTERNAL_AUTHORITY"
def test_tampered_ledger_cannot_be_evaluated(tmp_path):
 path=tmp_path/"ledger.json";ledger=ExternalEvidenceLedger();ledger.append(path,"R","EXT-VENDOR","license entitlement","Vendor","2026-08-03T00:00:00Z","evidence://x","a"*64,"https://vendor/verify/x");rows=ledger.load(path);rows[0]["issuer"]="Forged"
 try:ExternalGateManager().evaluate_ledger(rows,{"Vendor":"https://vendor/verify/"})
 except ValueError as exc:assert "external_evidence_ledger_invalid" in str(exc)
 else:assert False
