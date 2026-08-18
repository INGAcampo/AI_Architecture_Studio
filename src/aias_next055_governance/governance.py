from pathlib import Path
import json
class RoadmapGovernance:
 def __init__(self,plan:str|Path):self.path=Path(plan)
 def inspect(self):
  if not self.path.exists():return {'status':'HOLD'}
  p=json.loads(self.path.read_text(encoding='utf-8'));return {'status':'ACTIVE','rules':p.get('governing_rules',[]),'external_gates':'PENDING','production_approval':False}
