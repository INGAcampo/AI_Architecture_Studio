"""Append-only hash-chained engineering evidence ledger."""
from __future__ import annotations
import hashlib,json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path

class EngineeringEvidenceLedger:
    """Persist attributable engineering evidence in a tamper-evident hash chain."""
    def __init__(self,path:Path):self.path=path;self.data=self._load()
    def _load(self):return json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {"schema_version":"1.0.0","records":[]}
    def append(self,evidence_id:str,evidence_type:str,source:str,payload:dict,review_required:bool=True)->dict:
        """Append unique evidence with previous-record and canonical payload hashes."""
        if not all((evidence_id,evidence_type,source)) or any(x["evidence_id"]==evidence_id for x in self.data["records"]):raise ValueError("invalid_or_duplicate_evidence")
        previous=self.data["records"][-1]["record_sha256"] if self.data["records"] else "GENESIS";row={"sequence":len(self.data["records"])+1,"evidence_id":evidence_id,"evidence_type":evidence_type,"source":source,"payload":payload,"recorded_at":datetime.now(timezone.utc).isoformat(),"previous_sha256":previous,"professional_review_required":review_required};row["record_sha256"]=self._digest(row);self.data["records"].append(row);self._save();return row
    def verify(self)->dict:
        """Verify sequence, previous hashes and canonical record hashes."""
        issues=[];previous="GENESIS"
        for index,row in enumerate(self.data["records"],1):
            expected=self._digest({k:v for k,v in row.items() if k!="record_sha256"})
            if row["sequence"]!=index or row["previous_sha256"]!=previous or row["record_sha256"]!=expected:issues.append(row["evidence_id"])
            previous=row["record_sha256"]
        return {"valid":not issues,"records":len(self.data["records"]),"issues":issues}
    @staticmethod
    def _digest(row):return hashlib.sha256(json.dumps(row,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
    def _save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True);fd,name=tempfile.mkstemp(dir=self.path.parent,suffix=".tmp")
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as stream:json.dump(self.data,stream,ensure_ascii=False,indent=2,sort_keys=True);stream.write("\n")
            os.replace(name,self.path)
        finally:
            if os.path.exists(name):os.unlink(name)
