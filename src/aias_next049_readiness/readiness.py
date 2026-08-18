from pathlib import Path
import json
class StrategicReadiness:
 def __init__(self,plan:str|Path): self.path=Path(plan)
 def check(self):
  if not self.path.exists(): return {'ready':False,'reason':'plan absent'}
  p=json.loads(self.path.read_text(encoding='utf-8'));n=p.get('next');return {'ready':bool(n) and not str(n).startswith('DEFERRED:'),'next':n}
