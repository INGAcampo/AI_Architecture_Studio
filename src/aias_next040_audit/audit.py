from dataclasses import dataclass
from pathlib import Path
import json
@dataclass(frozen=True)
class ContinuityAudit:
    records: int
    malformed: int
    status: str
class ContinuityAuditor:
    def __init__(self,path:str|Path): self.path=Path(path)
    def run(self):
        if not self.path.exists(): return ContinuityAudit(0,0,'NO_EVIDENCE')
        malformed=0; count=0
        for line in self.path.read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            count+=1
            try: json.loads(line)
            except json.JSONDecodeError: malformed+=1
        return ContinuityAudit(count,malformed,'VALID' if malformed==0 else 'INVALID')
