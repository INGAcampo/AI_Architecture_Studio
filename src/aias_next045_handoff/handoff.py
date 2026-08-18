from pathlib import Path
import json
class RoadmapHandoff:
 def __init__(self,plan:str|Path): self.path=Path(plan)
 def build(self):
  if not self.path.exists(): return {'status':'INCOMPLETE','reason':'plan absent'}
  p=json.loads(self.path.read_text(encoding='utf-8'));return {'status':'READY_FOR_CONTINUATION','current':p.get('current'),'next':p.get('next'),'warnings':['external gates pending','production approval not granted']}
