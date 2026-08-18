from pathlib import Path
import json
class NextMacrodelivery:
 def __init__(self,plan:str|Path):self.path=Path(plan)
 def select(self):
  if not self.path.exists():return None
  p=json.loads(self.path.read_text(encoding='utf-8'));n=p.get('next');return n if n and not str(n).startswith('DEFERRED:') else None
