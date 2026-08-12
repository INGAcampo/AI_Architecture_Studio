"""Convert incomplete master-inventory concepts into dependency-aware PMO candidates."""
from __future__ import annotations
import json
from pathlib import Path
from .portfolio import PortfolioItem,PortfolioOffice
def from_master_inventory(office:PortfolioOffice,path:Path)->dict:
 """Register every specified, planned or partial concept as a governed PMO candidate."""
 rows=json.loads(path.read_text(encoding="utf-8"))["concepts"]
 for row in rows:
  if row["declared_state"] not in {"SPECIFIED","PLANNED","PARTIAL"}:continue
  operational_dependencies=[x for x in row.get("depends_on",[]) if any(y["id"]==x and y["declared_state"]=="OPERATIONAL" for y in rows)]
  office.add(PortfolioItem(row["id"],row["name"],[x for x in row.get("depends_on",[]) if x not in operational_dependencies],strategic_value=.8 if row["kind"] in {"FOUNDATION","SYSTEM"} else .65,urgency=max(.2,1-row["wave"]/25),reuse=.8 if row["kind"] in {"FOUNDATION","SYSTEM"} else .6,acceleration=.7,compliance=.75,risk=.5,effort=.6))
 return {"registered":len(office.items),"items":[x.to_dict() for x in office.items.values()]}
