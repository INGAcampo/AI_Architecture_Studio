from pathlib import Path
class EvidenceSummary:
 def __init__(self,root:str|Path): self.root=Path(root)
 def build(self):
  installers=sum(1 for p in self.root.iterdir() if p.is_dir() and p.name.startswith('AIAS_NEXT') and p.name.endswith('INSTALLER')) if self.root.exists() else 0
  return {'installers_detected':installers,'external_approval':'PENDING','production_release':False}
