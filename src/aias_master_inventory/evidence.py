"""Repository reconciliation for declared concept states."""
from pathlib import Path
def reconcile(root:Path,rows:list[dict])->list[dict]:
 """Attach evidence existence and flag unsupported operational declarations."""
 result=[]
 for row in rows:
  copy=dict(row);copy["evidence_exists"]=bool(row["evidence"] and (root/row["evidence"]).exists());copy["supported"]=row["declared_state"] not in {"OPERATIONAL","PARTIAL"} or copy["evidence_exists"];result.append(copy)
 return result
