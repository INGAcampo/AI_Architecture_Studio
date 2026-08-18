from dataclasses import dataclass,field,asdict
from datetime import datetime,timezone
import uuid
def utc_now_iso(): return datetime.now(timezone.utc).isoformat()
@dataclass
class ProjectMetadata:
    name:str="Sin título"
    project_id:str=field(default_factory=lambda:str(uuid.uuid4()))
    author:str=""; company:str=""; description:str=""
    created_utc:str=field(default_factory=utc_now_iso)
    modified_utc:str=field(default_factory=utc_now_iso)
    def touch(self): self.modified_utc=utc_now_iso()
    def to_dict(self): return asdict(self)
    @classmethod
    def from_dict(cls,data):
        allowed=cls.__dataclass_fields__.keys(); return cls(**{k:v for k,v in data.items() if k in allowed})
