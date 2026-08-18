from pathlib import Path
import json
class MonitorReport:
 def __init__(self,plan:str|Path):self.path=Path(plan)
 def build(self):
  if not self.path.exists():return {'status':'HOLD','mutated':False}
  p=json.loads(self.path.read_text(encoding='utf-8'));return {'status':'OBSERVED','current':p.get('current'),'next':p.get('next'),'mutated':False,'external_gates':'PENDING'}
