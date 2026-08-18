from pathlib import Path
class IntegrityReport:
 def __init__(self,path:str|Path):self.path=Path(path)
 def build(self):
  if not self.path.exists():return {'status':'NO_ARCHIVE','valid':False}
  return {'status':'PRESENT','valid':True,'records':len([x for x in self.path.read_text(encoding='utf-8').splitlines() if x.strip()])}
