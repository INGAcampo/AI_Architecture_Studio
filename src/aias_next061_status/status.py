from pathlib import Path
import json
class RoadmapStatus:
 def __init__(self,plan:str|Path):self.path=Path(plan)
 def read(self):
  if not self.path.exists():return {'status':'HOLD'}
  p=json.loads(self.path.read_text(encoding='utf-8'));return {'status':'ACTIVE','current':p.get('current'),'next':p.get('next'),'external_gates':'PENDING','global_completion':False}
