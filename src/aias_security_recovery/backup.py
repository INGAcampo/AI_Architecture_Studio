"""Signed snapshot creation, verification, safe restoration and recovery drills."""
from __future__ import annotations
import hashlib,hmac,json,time,zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
from .policy import SecurityRecoveryPolicy
from .scanner import SecurityScanner

class BackupManager:
    """Create deterministic attributable backups and prove they can be restored."""
    def __init__(self,policy:SecurityRecoveryPolicy|None=None,scanner:SecurityScanner|None=None):self.policy=policy or SecurityRecoveryPolicy();self.scanner=scanner or SecurityScanner(self.policy);self.policy.validate()
    def create(self,source:Path,output:Path,snapshot_id:str,signing_key:bytes)->dict:
        """Create a ZIP snapshot excluding secrets and sign its canonical manifest."""
        source=source.resolve();output=output.resolve()
        if not source.is_dir() or not snapshot_id.startswith("SNP-") or len(signing_key)<32:raise ValueError("invalid_backup_request")
        output.parent.mkdir(parents=True,exist_ok=True);files=[];excluded=[]
        with zipfile.ZipFile(output,"w",zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(source.rglob("*")):
                if not path.is_file() and not path.is_symlink():continue
                rel=path.relative_to(source).as_posix();reason=self.scanner.exclusion_reason(path)
                if reason:excluded.append({"path":rel,"reason":reason});continue
                data=path.read_bytes();issues=self.scanner.scan_text(data.decode("utf-8",errors="ignore"))
                if issues:excluded.append({"path":rel,"reason":"embedded_secret"});continue
                digest=hashlib.sha256(data).hexdigest();files.append({"path":rel,"size":len(data),"sha256":digest});bundle.writestr(rel,data)
            manifest={"schema_version":"1.0.0","snapshot_id":snapshot_id,"created_at":datetime.now(timezone.utc).isoformat(),"source_name":source.name,"algorithm":"HMAC-SHA256","files":files,"excluded":excluded,"rpo_minutes":self.policy.rpo_minutes,"rto_minutes":self.policy.rto_minutes}
            canonical=json.dumps(manifest,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode();signature=hmac.new(signing_key,canonical,hashlib.sha256).hexdigest();bundle.writestr(".aias_recovery/manifest.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n");bundle.writestr(".aias_recovery/signature.hmac",signature+"\n")
        return {"snapshot_id":snapshot_id,"archive":str(output),"files":len(files),"excluded":excluded,"sha256":hashlib.sha256(output.read_bytes()).hexdigest(),"verified":self.verify(output,signing_key)["valid"],"created_at":manifest["created_at"]}
    def verify(self,archive:Path,signing_key:bytes)->dict:
        """Verify signature, allowed member paths, sizes and every file digest."""
        issues=[]
        try:
            with zipfile.ZipFile(archive) as bundle:
                names=set(bundle.namelist());manifest=json.loads(bundle.read(".aias_recovery/manifest.json"));signature=bundle.read(".aias_recovery/signature.hmac").decode().strip();canonical=json.dumps(manifest,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
                if not hmac.compare_digest(signature,hmac.new(signing_key,canonical,hashlib.sha256).hexdigest()):issues.append("invalid_signature")
                for row in manifest["files"]:
                    if not self._safe(row["path"]) or row["path"] not in names:issues.append(f"invalid_member:{row['path']}");continue
                    data=bundle.read(row["path"])
                    if len(data)!=row["size"] or hashlib.sha256(data).hexdigest()!=row["sha256"]:issues.append(f"integrity_failure:{row['path']}")
        except (KeyError,ValueError,zipfile.BadZipFile,json.JSONDecodeError):issues.append("invalid_archive")
        return {"valid":not issues,"issues":issues}
    def restore(self,archive:Path,destination:Path,signing_key:bytes)->dict:
        """Restore verified regular files into a new empty recovery destination."""
        verification=self.verify(archive,signing_key)
        if not verification["valid"]:raise ValueError("unverified_backup")
        destination=destination.resolve()
        if destination.exists() and any(destination.iterdir()):raise ValueError("restore_destination_not_empty")
        destination.mkdir(parents=True,exist_ok=True);restored=[]
        with zipfile.ZipFile(archive) as bundle:
            manifest=json.loads(bundle.read(".aias_recovery/manifest.json"))
            for row in manifest["files"]:
                target=(destination/row["path"]).resolve()
                if destination not in target.parents:raise ValueError("unsafe_restore_path")
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(bundle.read(row["path"]));restored.append(row["path"])
        return {"snapshot_id":manifest["snapshot_id"],"destination":str(destination),"restored":len(restored)}
    def drill(self,archive:Path,drill_destination:Path,signing_key:bytes)->dict:
        """Measure a full verified restore and report recovery-objective evidence."""
        started=time.perf_counter();result=self.restore(archive,drill_destination,signing_key);seconds=time.perf_counter()-started;result.update({"recovery_seconds":seconds,"rto_met":seconds/60<=self.policy.rto_minutes,"verified":True});return result
    @staticmethod
    def _safe(name:str)->bool:
        path=PurePosixPath(name);return not path.is_absolute() and ".." not in path.parts and not name.startswith(("/","\\"))
