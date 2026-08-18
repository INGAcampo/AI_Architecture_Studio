from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json
@dataclass(frozen=True)
class ArchiveEntry:
    recorded_at: str
    source: str
    sha256: str
class ContinuityArchive:
    def __init__(self, archive_path: str|Path): self.path=Path(archive_path)
    def append(self, source: str|Path):
        p=Path(source); digest=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else ""
        e=ArchiveEntry(datetime.now(timezone.utc).isoformat(),str(p),digest); self.path.parent.mkdir(parents=True,exist_ok=True); self.path.open('a',encoding='utf-8').write(json.dumps(asdict(e))+'\n'); return e
