"""Fail-closed version update planning without implicit downloads or downgrades."""
from __future__ import annotations
import re
SEMVER=re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
class UpdatePlanner:
 def plan(self,current:str,candidate:str,*,candidate_integrity_verified:bool,publisher_signature_verified:bool,allow_downgrade:bool=False)->dict:
  if not SEMVER.fullmatch(current) or not SEMVER.fullmatch(candidate):raise ValueError("invalid_semver")
  old=tuple(map(int,current.split(".")));new=tuple(map(int,candidate.split(".")))
  blockers=[]
  if not candidate_integrity_verified:blockers.append("candidate_integrity_unverified")
  if not publisher_signature_verified:blockers.append("publisher_signature_unverified")
  if new<old and not allow_downgrade:blockers.append("downgrade_not_allowed")
  if new==old:blockers.append("same_version")
  return {"current":current,"candidate":candidate,"action":"INSTALL" if not blockers else "BLOCKED","blockers":blockers,"requires_recovery_point":True,"automatic_download_authorized":False}
