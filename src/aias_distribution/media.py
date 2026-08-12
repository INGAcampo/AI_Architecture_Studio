"""Deterministic offline distribution media with truthful signing status."""
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path,PurePosixPath

def _safe(name:str)->bool:
 path=PurePosixPath(name);return bool(name) and not path.is_absolute() and ".." not in path.parts and not name.startswith(("/","\\"))

def _installer_valid(path:Path)->dict:
 checks=path/"checksums.sha256";issues=[]
 if not checks.is_file():return {"valid":False,"issues":["missing_checksums"]}
 for line in checks.read_text(encoding="utf-8").splitlines():
  if not line.strip():continue
  parts=line.split("  ",1)
  if len(parts)!=2 or not _safe(parts[1]):issues.append("invalid_checksum_line");continue
  source=path/parts[1]
  if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest()!=parts[0]:issues.append(f"checksum:{parts[1]}")
 return {"valid":not issues,"issues":issues}

class OfflineMediaBuilder:
 def build(self,root:Path,installer_names:tuple[str,...],output:Path,version:str)->dict:
  root=root.resolve();output=output.resolve();rows=[]
  if not version or not installer_names:raise ValueError("invalid_offline_media_request")
  for name in installer_names:
   if Path(name).name!=name:raise ValueError("invalid_installer_name")
   folder=root/name;result=_installer_valid(folder)
   if not folder.is_dir() or not result["valid"]:raise ValueError(f"invalid_installer:{name}:{','.join(result['issues'])}")
   rows.append((name,folder))
  output.parent.mkdir(parents=True,exist_ok=True);files=[]
  with zipfile.ZipFile(output,"w",zipfile.ZIP_DEFLATED,strict_timestamps=False) as bundle:
   for name,folder in sorted(rows):
    for source in sorted(path for path in folder.rglob("*") if path.is_file()):
     relative=f"installers/{name}/{source.relative_to(folder).as_posix()}";data=source.read_bytes();files.append({"path":relative,"size":len(data),"sha256":hashlib.sha256(data).hexdigest()});info=zipfile.ZipInfo(relative,(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;bundle.writestr(info,data)
   manifest={"schema":"AIAS-OFFLINE-MEDIA-1.0","product":"AI Architecture Studio","version":version,"format":"REPRODUCIBLE_OFFLINE_ZIP","iso_image_created":False,"publisher_signature":{"status":"NOT_CONFIGURED","reason":"publisher certificate and external signing authority not supplied"},"integrity":"SHA-256","installers":[name for name,_ in sorted(rows)],"files":files,"created_at":"2026-01-01T00:00:00+00:00","build_epoch_policy":"FIXED_PER_RELEASE_VERSION"}
   canonical=json.dumps({k:v for k,v in manifest.items() if k!="created_at"},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode();manifest["content_sha256"]=hashlib.sha256(canonical).hexdigest();bundle.writestr(zipfile.ZipInfo("MEDIA_MANIFEST.json",(2026,1,1,0,0,0)),json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
  verification=verify_offline_media(output);return {"media":str(output),"sha256":hashlib.sha256(output.read_bytes()).hexdigest(),"installers":len(rows),"files":len(files),"verified":verification["valid"],"publisher_signed":False,"iso_image_created":False}

def verify_offline_media(path:Path)->dict:
 issues=[]
 try:
  with zipfile.ZipFile(path) as bundle:
   names=set(bundle.namelist());manifest=json.loads(bundle.read("MEDIA_MANIFEST.json"))
   for row in manifest["files"]:
    if not _safe(row["path"]) or row["path"] not in names:issues.append(f"invalid_member:{row['path']}");continue
    data=bundle.read(row["path"])
    if len(data)!=row["size"] or hashlib.sha256(data).hexdigest()!=row["sha256"]:issues.append(f"integrity:{row['path']}")
   canonical=json.dumps({k:v for k,v in manifest.items() if k not in {"created_at","content_sha256"}},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
   if hashlib.sha256(canonical).hexdigest()!=manifest.get("content_sha256"):issues.append("manifest_integrity")
 except (OSError,KeyError,ValueError,json.JSONDecodeError,zipfile.BadZipFile):issues.append("invalid_media")
 return {"valid":not issues,"issues":issues}
