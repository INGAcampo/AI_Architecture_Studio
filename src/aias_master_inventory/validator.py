"""Structural integrity controls for the canonical inventory."""
from __future__ import annotations
import re
STATES={"OPERATIONAL","PARTIAL","SPECIFIED","PLANNED","SUPERSEDED","DUPLICATE"};KINDS={"RULE","FOUNDATION","SYSTEM","OFFICE","ENGINEERING_CAPABILITY","FUTURE_VISION","DUPLICATE"};IDENTIFIER=re.compile(r"^[A-Z]+-\d{6}$")
def validate(rows:list[dict])->list[str]:
 """Return identifier, state, classification and dependency errors."""
 errors=[];ids=[r["id"] for r in rows];known=set(ids)
 if len(ids)!=len(known):errors.append("duplicate_identifiers")
 for row in rows:
  if not IDENTIFIER.fullmatch(row["id"]):errors.append(f"invalid_id:{row['id']}")
  if row["declared_state"] not in STATES:errors.append(f"invalid_state:{row['id']}")
  if row["kind"] not in KINDS:errors.append(f"invalid_kind:{row['id']}")
  for dep in row["depends_on"]:
   if dep not in known:errors.append(f"unknown_dependency:{row['id']}:{dep}")
 return errors
