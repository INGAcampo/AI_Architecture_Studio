from pathlib import Path
import json
class StrategicEvidenceReview:
 def __init__(self,path:str|Path): self.path=Path(path)
 def run(self):
  if not self.path.exists(): return {'status':'NO_EVIDENCE','valid':False}
  rows=[json.loads(x) for x in self.path.read_text(encoding='utf-8').splitlines() if x.strip()];return {'status':'REVIEWED','valid':all(r.get('item') and r.get('status') for r in rows),'count':len(rows)}
