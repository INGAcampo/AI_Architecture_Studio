from pathlib import Path
import json
class StrategicSelector:
 def __init__(self,plan:str|Path): self.path=Path(plan)
 def select(self):
  if not self.path.exists(): return {'status':'HOLD'}
  p=json.loads(self.path.read_text(encoding='utf-8')); b=[x for x in p.get('backlog',[]) if not str(x).startswith('DEFERRED:')]; return {'status':'SELECTED' if b else 'HOLD','item':b[0] if b else None}
