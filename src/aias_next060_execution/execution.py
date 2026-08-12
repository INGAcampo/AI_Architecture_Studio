from pathlib import Path
import json
class ExecutionContinuation:
 def __init__(self,plan:str|Path):self.path=Path(plan)
 def check(self):
  if not self.path.exists():return {'status':'HOLD'}
  p=json.loads(self.path.read_text(encoding='utf-8'));return {'status':'READY','next':p.get('next'),'external_gates':'PENDING'}
