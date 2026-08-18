"""Staged installation with explicit destination boundaries and recoverable rollback."""
from __future__ import annotations
import shutil,uuid,zipfile
from dataclasses import dataclass
from pathlib import Path,PurePosixPath
from .media import verify_offline_media

@dataclass(frozen=True)
class DeploymentPolicy:
 allowed_root:Path
 retain_previous:bool=True
 def validate_destination(self,destination:Path)->Path:
  root=self.allowed_root.resolve();target=destination.resolve()
  if target==root or root not in target.parents:raise ValueError("destination_outside_allowed_root")
  if len(target.parts)<=2:raise ValueError("destination_too_broad")
  return target

class InstallerTransaction:
 def __init__(self,policy:DeploymentPolicy):self.policy=policy
 def install(self,media:Path,destination:Path)->dict:
  verification=verify_offline_media(media)
  if not verification["valid"]:raise ValueError("unverified_offline_media")
  target=self.policy.validate_destination(destination);token=uuid.uuid4().hex;stage=target.parent/f".{target.name}.stage-{token}";backup=target.parent/f".{target.name}.previous-{token}"
  if stage.exists() or backup.exists():raise RuntimeError("transaction_path_collision")
  stage.mkdir(parents=True)
  try:
   with zipfile.ZipFile(media) as bundle:
    for info in bundle.infolist():
     relative=PurePosixPath(info.filename)
     if relative.is_absolute() or ".." in relative.parts:raise ValueError("unsafe_media_member")
     if info.is_dir():continue
     output=(stage/Path(*relative.parts)).resolve()
     if stage.resolve() not in output.parents:raise ValueError("unsafe_media_member")
     output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(bundle.read(info))
   if target.exists():target.replace(backup)
   stage.replace(target)
  except Exception:
   if stage.exists():shutil.rmtree(stage)
   if backup.exists() and not target.exists():backup.replace(target)
   raise
  return {"status":"INSTALLED","destination":str(target),"previous":str(backup) if backup.exists() else None,"rollback_available":backup.exists(),"publisher_signed":False,"integrity_verified":True}
 def rollback(self,destination:Path,previous:Path)->dict:
  target=self.policy.validate_destination(destination);backup=self.policy.validate_destination(previous)
  if not backup.is_dir():raise ValueError("previous_release_missing")
  displaced=target.parent/f".{target.name}.superseded-{uuid.uuid4().hex}"
  if target.exists():target.replace(displaced)
  try:backup.replace(target)
  except Exception:
   if displaced.exists() and not target.exists():displaced.replace(target)
   raise
  return {"status":"ROLLED_BACK","destination":str(target),"superseded":str(displaced) if displaced.exists() else None}
