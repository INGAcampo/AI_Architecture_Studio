"""Public module supporting the universal engineering asset registry."""
from __future__ import annotations
import json,re,tempfile,os
from datetime import datetime,timezone
from pathlib import Path
ID=re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$");SEMVER=re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
STATES=("PROPOSED","SPECIFIED","IMPLEMENTED","VALIDATED","RELEASED","OPERATED","RETIRED")
REQUIRED={"id","title","asset_type","version","status","owner","purpose","scope","source","requirements","evidence","dependencies","legal_status"}
class AssetRegistryError(ValueError):
 """Raised when an asset violates identity, lifecycle or dependency invariants."""
class AssetRegistry:
 """Execute the public AssetRegistry operation for the universal engineering asset registry using explicit caller inputs."""
 def __init__(self,path:Path):self.path=path;self.data=self._load()
 def _load(self):
  if not self.path.exists():return {"schema_version":"1.0.0","assets":{},"events":[]}
  return json.loads(self.path.read_text(encoding="utf-8"))
 def _validate(self,a):
  issues=[f"missing:{x}" for x in sorted(REQUIRED-set(a))]
  if not ID.fullmatch(a.get("id","")):issues.append("invalid_id")
  if not SEMVER.fullmatch(a.get("version","")):issues.append("invalid_version")
  if a.get("status") not in STATES:issues.append("invalid_status")
  unknown=set(a.get("dependencies",[]))-set(self.data["assets"])
  if unknown:issues.append(f"unknown_dependencies:{sorted(unknown)}")
  if issues:raise AssetRegistryError(";".join(issues))
 def _save(self):
  self.path.parent.mkdir(parents=True,exist_ok=True);fd,name=tempfile.mkstemp(dir=self.path.parent,suffix=".tmp")
  try:
   with os.fdopen(fd,"w",encoding="utf-8") as f:json.dump(self.data,f,ensure_ascii=False,indent=2);f.write("\n")
   os.replace(name,self.path)
  finally:
   if os.path.exists(name):os.unlink(name)
 def register(self,asset,actor="SYSTEM"):
  """Add register to the universal engineering asset registry while enforcing identity constraints."""
  self._validate(asset)
  if asset["id"] in self.data["assets"]:raise AssetRegistryError("duplicate_id")
  self.data["assets"][asset["id"]]=dict(asset);self._event("REGISTER",asset["id"],actor);self._save();return asset
 def transition(self,asset_id,status,actor,reason):
  """Execute the public AssetRegistry.transition operation for the universal engineering asset registry using explicit caller inputs."""
  asset=self.data["assets"].get(asset_id)
  if not asset:raise AssetRegistryError("unknown_asset")
  if status not in STATES or STATES.index(status)!=STATES.index(asset["status"])+1:raise AssetRegistryError("invalid_transition")
  asset["status"]=status;self._event("TRANSITION",asset_id,actor,{"status":status,"reason":reason});self._save();return asset
 def query(self,asset_type=None,status=None):
  """Return assets filtered by optional type and lifecycle status."""
  return [a for a in self.data["assets"].values() if (not asset_type or a["asset_type"]==asset_type) and (not status or a["status"]==status)]
 def _event(self,kind,asset_id,actor,details=None):self.data["events"].append({"event":kind,"asset_id":asset_id,"actor":actor,"timestamp":datetime.now(timezone.utc).isoformat(),"details":details or {}})
