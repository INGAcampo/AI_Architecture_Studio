import json
from aias_roadmap_audit.cli import main
H="a"*64
def registry(path):path.write_text(json.dumps({"authorities":{"Publisher":"https://authority/verify/"}}))
def test_cli_validates_empty_ledger(tmp_path,capsys):
 ledger=tmp_path/"ledger.json";ledger.write_text('{"records":[]}');assert main(["--ledger",str(ledger),"validate"])==0;assert json.loads(capsys.readouterr().out)["valid"] is True
def test_cli_appends_real_evidence_and_reports_status(tmp_path,capsys):
 ledger=tmp_path/"ledger.json";authorities=tmp_path/"authorities.json";registry(authorities)
 args=["--ledger",str(ledger),"append","--record-id","R1","--gate-id","EXT-NORMATIVE","--evidence-type","purchase authorization","--issuer","Publisher","--issued-at","2026-08-03T00:00:00Z","--artifact-locator","evidence://1","--artifact-sha256",H,"--authority-verification-reference","https://authority/verify/1"]
 assert main(args)==0;capsys.readouterr();assert main(["--ledger",str(ledger),"--authorities",str(authorities),"status"])==0;out=json.loads(capsys.readouterr().out);assert out["status"]=="WAITING_EXTERNAL_AUTHORITIES"
def test_cli_rejects_tampered_ledger(tmp_path,capsys):
 ledger=tmp_path/"ledger.json";ledger.write_text('{"records":[{"record_id":"x"}]}');assert main(["--ledger",str(ledger),"validate"])==1;assert json.loads(capsys.readouterr().out)["valid"] is False
