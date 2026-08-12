from pathlib import Path
class StrategicContinuityCheckpoint:
 def __init__(self,root:str|Path):self.root=Path(root)
 def run(self):
  required=[self.root/'engineering/aias/master/AIAS_MASTER_DEVELOPMENT_PLAN.json',self.root/'ACKC/MASTER_CONTEXT.json'];ok=all(p.exists() for p in required);return {'status':'CONTINUE' if ok else 'HOLD','external_gates':'PENDING'}
