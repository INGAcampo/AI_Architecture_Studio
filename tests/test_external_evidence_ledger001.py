import json
from aias_roadmap_audit import ExternalEvidenceLedger
H="a"*64
def test_external_evidence_is_hash_chained_and_reloadable(tmp_path):
 p=tmp_path/"ledger.json";ledger=ExternalEvidenceLedger();a=ledger.append(p,"R1","EXT-NORMATIVE","license","Publisher","2026-08-03T00:00:00Z","evidence://license",H,"authority://verification/1");b=ledger.append(p,"R2","EXT-BENCHMARK","review","Engineer","2026-08-03T01:00:00Z","evidence://review",H,"authority://verification/2");rows=ledger.load(p);assert b.previous_hash==a.record_hash and ledger.validate(rows)==[]
def test_tampering_is_detected(tmp_path):
 p=tmp_path/"ledger.json";ledger=ExternalEvidenceLedger();ledger.append(p,"R","EXT-VENDOR","license","Vendor","2026-08-03T00:00:00Z","evidence://vendor",H,"vendor://verify");data=json.loads(p.read_text());data["records"][0]["issuer"]="Forged";assert "0:record_hash_invalid" in ledger.validate(data["records"])
def test_unknown_gate_and_missing_authority_verification_are_rejected(tmp_path):
 ledger=ExternalEvidenceLedger();p=tmp_path/"ledger.json"
 try:ledger.append(p,"R","UNKNOWN","x","x","2026-08-03T00:00:00Z","x",H,"x")
 except ValueError as exc:assert str(exc)=="unsupported_gate"
 else:assert False
 try:ledger.append(p,"R","EXT-MATURITY","x","x","2026-08-03T00:00:00Z","x",H,"")
 except ValueError as exc:assert str(exc)=="external_evidence_incomplete"
 else:assert False
