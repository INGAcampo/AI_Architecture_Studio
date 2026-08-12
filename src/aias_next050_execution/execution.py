from datetime import datetime,timezone
from pathlib import Path
import json
class StrategicExecution:
 def __init__(self,path:str|Path): self.path=Path(path)
 def record(self,item:str,status='STARTED'):
  row={'recorded_at':datetime.now(timezone.utc).isoformat(),'item':item,'status':status,'release_approved':False};self.path.parent.mkdir(parents=True,exist_ok=True);self.path.open('a',encoding='utf-8').write(json.dumps(row)+'\n');return row
