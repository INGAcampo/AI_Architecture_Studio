from pathlib import Path
from datetime import datetime,timezone
import json
class ExecutionLedger:
 def __init__(self,path:str|Path): self.path=Path(path)
 def append(self,macrodelivery:str,status:str,evidence:str=''):
  row={'recorded_at':datetime.now(timezone.utc).isoformat(),'macrodelivery':macrodelivery,'status':status,'evidence':evidence};self.path.parent.mkdir(parents=True,exist_ok=True);self.path.open('a',encoding='utf-8').write(json.dumps(row)+'\n');return row
