"""Command-line capture and verification for the Level 5 evidence campaign."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .ledger import EvidenceLedger


def _ledger(args: argparse.Namespace) -> EvidenceLedger:
    """Create the ledger using an external key supplied through the environment."""
    key = os.environ.get(args.key_env, "").encode("utf-8")
    return EvidenceLedger(Path(args.ledger), key)


def main(argv: list[str] | None = None) -> int:
    """Record evidence or report authenticated campaign progress."""
    parser = argparse.ArgumentParser(prog="aias-level5-evidence")
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--key-env", default="AIAS_LEVEL5_SIGNING_KEY")
    commands = parser.add_subparsers(dest="command", required=True)
    record = commands.add_parser("record")
    record.add_argument("--event", required=True)
    record.add_argument("--evidence-id", required=True)
    record.add_argument("--observed-at", required=True)
    record.add_argument("--payload", required=True, help="JSON object; record only verified real observations")
    commands.add_parser("verify")
    commands.add_parser("status")
    args = parser.parse_args(argv)
    ledger = _ledger(args)
    if args.command == "record":
        result = ledger.append(args.event, json.loads(args.payload), args.observed_at, evidence_id=args.evidence_id)
    elif args.command == "verify":
        result = ledger.verify()
    else:
        result = ledger.campaign_status()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
