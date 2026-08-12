from pathlib import Path
import json
class DashboardSync:
 def __init__(self,plan:str|Path,dashboard:str|Path): self.plan=Path(plan);self.dashboard=Path(dashboard)
 def run(self):
  if not self.plan.exists() or not self.dashboard.exists(): return {'status':'HOLD'}
  p=json.loads(self.plan.read_text(encoding='utf-8'));d=json.loads(self.dashboard.read_text(encoding='utf-8'));return {'status':'SYNCHRONIZED','next':p.get('next'),'dashboard_valid':d.get('validated',True)}
