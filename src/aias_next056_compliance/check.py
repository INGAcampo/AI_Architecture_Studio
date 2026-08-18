from pathlib import Path
class ComplianceCheck:
 def __init__(self,root:str|Path):self.root=Path(root)
 def run(self):
  req=['engineering/aias/master/AIAS_MASTER_DEVELOPMENT_PLAN.json','ACKC/MASTER_CONTEXT.json'];missing=[x for x in req if not (self.root/x).exists()];return {'status':'COMPLIANT' if not missing else 'NON_COMPLIANT','missing':missing}
