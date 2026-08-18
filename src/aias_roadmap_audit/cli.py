"""CLI for authenticated external evidence operations."""
from __future__ import annotations
import argparse,json
from dataclasses import asdict
from pathlib import Path
from .evidence import ExternalEvidenceLedger
from .external_gates import ExternalGateManager

def main(argv=None):
 p=argparse.ArgumentParser(prog="aias-external-gates");p.add_argument("--ledger",default="engineering/aias/roadmap/EXTERNAL_EVIDENCE_LEDGER.json");p.add_argument("--authorities",default="engineering/aias/roadmap/EXTERNAL_AUTHORITY_REGISTRY.json");commands=p.add_subparsers(dest="command",required=True)
 commands.add_parser("validate");commands.add_parser("status")
 add=commands.add_parser("append")
 for name in ("record-id","gate-id","evidence-type","issuer","issued-at","artifact-locator","artifact-sha256","authority-verification-reference"):add.add_argument(f"--{name}",required=True)
 a=p.parse_args(argv);ledger_path=Path(a.ledger).resolve();ledger=ExternalEvidenceLedger()
 if a.command=="append":
  row=ledger.append(ledger_path,a.record_id,a.gate_id,a.evidence_type,a.issuer,a.issued_at,a.artifact_locator,a.artifact_sha256,a.authority_verification_reference);print(json.dumps(asdict(row),indent=2));return 0
 records=ledger.load(ledger_path);issues=ledger.validate(records)
 if a.command=="validate":print(json.dumps({"valid":not issues,"issues":issues,"records":len(records)},indent=2));return 0 if not issues else 1
 if issues:print(json.dumps({"status":"INVALID_LEDGER","issues":issues},indent=2));return 1
 authority_path=Path(a.authorities).resolve();registry=json.loads(authority_path.read_text(encoding="utf-8"));portfolio=ExternalGateManager().evaluate_ledger(records,registry.get("authorities",{}));print(json.dumps(asdict(portfolio),indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
