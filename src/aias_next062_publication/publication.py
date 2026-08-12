from pathlib import Path
import json
class RoadmapPublication:
 def __init__(self,plan:str|Path):self.path=Path(plan)
 def publish(self):
  if not self.path.exists():return {'status':'HOLD'}
  p=json.loads(self.path.read_text(encoding='utf-8'));return {'status':'PUBLISHED_REFERENCE','current':p.get('current'),'next':p.get('next'),'release':False}
