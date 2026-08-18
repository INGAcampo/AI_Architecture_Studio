from pathlib import Path
import hashlib
class ArchiveMonitorReport:
 def __init__(self,path:str|Path):self.path=Path(path)
 def build(self):
  if not self.path.exists():return {'status':'NO_ARCHIVE','mutated':False}
  return {'status':'OBSERVED','sha256':hashlib.sha256(self.path.read_bytes()).hexdigest(),'mutated':False}
