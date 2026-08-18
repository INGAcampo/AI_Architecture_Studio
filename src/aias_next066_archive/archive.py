from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
class RoadmapArchive:
 def __init__(self,archive:str|Path):self.archive=Path(archive)
 def add(self,source:str|Path):
  p=Path(source);row={'recorded_at':datetime.now(timezone.utc).isoformat(),'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else ''};self.archive.parent.mkdir(parents=True,exist_ok=True);self.archive.open('a',encoding='utf-8').write(json.dumps(row)+'\n');return row
