"""Command-line execution of normalized continuous-observatory ingestion cycles."""
from __future__ import annotations
import argparse,json
from datetime import datetime
from pathlib import Path
from .engine import ContinuousObservatory
from .models import FeedItem
from .registry import SourceRegistry
def main()->int:
 """Run a scheduled ATO cycle from an adapter-normalized JSON batch."""
 parser=argparse.ArgumentParser(prog="aias-ato-continuous");parser.add_argument("--registry",default="engineering/aias/ato/ATO_CONTINUOUS_SOURCE_REGISTRY.json");parser.add_argument("--ledger",default=".aias/ato/continuous_ledger.json");parser.add_argument("--batch",required=True);parser.add_argument("--now");args=parser.parse_args()
 batch=json.loads(Path(args.batch).read_text(encoding="utf-8"));grouped={sid:[FeedItem(**row) for row in rows] for sid,rows in batch.items()};engine=ContinuousObservatory(SourceRegistry(Path(args.registry)),Path(args.ledger));result=engine.run_cycle(lambda source:grouped.get(source["id"],[]),datetime.fromisoformat(args.now) if args.now else None);print(json.dumps(result,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
