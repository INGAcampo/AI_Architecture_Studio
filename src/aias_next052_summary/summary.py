from pathlib import Path
import json
class StrategicSummary:
 def __init__(self,path:str|Path):self.path=Path(path)
 def build(self):
  if not self.path.exists():return {'count':0,'approval':'PENDING'}
  rows=[json.loads(x) for x in self.path.read_text(encoding='utf-8').splitlines() if x.strip()];return {'count':len(rows),'approval':'PENDING'}
