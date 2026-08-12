from pathlib import Path
import json
class MonitorPublication:
 def __init__(self,report:str|Path):self.path=Path(report)
 def publish(self):
  if not self.path.exists():return {'status':'HOLD','release':False}
  return {'status':'REFERENCE_PUBLICATION','release':False,'external_gates':'PENDING'}
