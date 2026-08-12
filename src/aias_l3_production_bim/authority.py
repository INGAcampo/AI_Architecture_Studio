"""Read the immutable authority map produced by L3-PRODUCTION-BIM-001A."""
from __future__ import annotations
from pathlib import Path
import json
class AuthorityMap:
    """Query ranked native authority candidates discovered by 001A."""
    def __init__(self,path:Path):
        self.path=Path(path); self.data=json.loads(self.path.read_text(encoding="utf-8-sig"))
    def top(self,domain:str):
        """Return the highest-ranked candidate for one domain."""
        rows=self.data.get("authority_map",{}).get(domain,[])
        return rows[0] if rows else None
    def require(self,*domains:str):
        """Require a top candidate for every requested domain."""
        result={d:self.top(d) for d in domains}
        missing=[d for d,v in result.items() if v is None]
        if missing: raise RuntimeError("missing_authority_domains:"+",".join(missing))
        return result
