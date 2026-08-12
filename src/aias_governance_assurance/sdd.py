"""Executable checks for the approved SDD lifecycle."""
from pathlib import Path
REQUIRED=("ASDD.json","TRACEABILITY.json","QUALITY_GATES.json")
def audit_compliance(root:Path)->dict:
 """Audit every discovered constitutional compliance pack."""
 rows=[]
 for folder in sorted((root/"engineering").glob("*/compliance")):
  missing=[name for name in REQUIRED if not (folder/name).is_file()]
  adr=bool(list(folder.glob("ADR-*.md")));arch=bool(list(folder.glob("ARCH-*.md")))
  rows.append({"component":folder.parent.name,"complete":not missing and adr and arch,"missing":missing+([] if adr else ["ADR"])+([] if arch else ["ARCH"])})
 return {"components":rows,"complete_count":sum(r["complete"] for r in rows),"component_count":len(rows),"all_complete":bool(rows) and all(r["complete"] for r in rows)}
