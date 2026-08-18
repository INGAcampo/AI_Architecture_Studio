from pathlib import Path
import json
class ContinuityValidation:
 def __init__(self,root:str|Path): self.root=Path(root)
 def run(self):
  plan=self.root/'engineering/aias/master/AIAS_MASTER_DEVELOPMENT_PLAN.json'; ace=self.root/'ACKC/MASTER_CONTEXT.json'
  ok=plan.exists() and ace.exists(); return {'status':'VALID' if ok else 'HOLD','external_gates':'PENDING','production_approval':False}
