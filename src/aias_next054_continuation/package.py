from pathlib import Path
import json
class ContinuationPackage:
 def __init__(self,plan:str|Path):self.path=Path(plan)
 def build(self):
  if not self.path.exists():return {'status':'INCOMPLETE'}
  p=json.loads(self.path.read_text(encoding='utf-8'));return {'status':'READY','current':p.get('current'),'next':p.get('next'),'warnings':['external gates pending','production approval not granted']}
