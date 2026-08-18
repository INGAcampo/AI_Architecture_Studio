import json
from pathlib import Path
from aias_roadmap_audit import HistoricalDecisionReconciler
ROOT=Path(__file__).resolve().parents[1];target=ROOT/"engineering/aias/roadmap/ROADMAP_RECONCILIATION_002.json";report=HistoricalDecisionReconciler().write(ROOT,target);print(json.dumps({"target":str(target),"status":report["status"],"next":report["next"],"sha256":report["sha256"]}))
