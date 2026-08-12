from pathlib import Path
import hashlib
class ArchiveMonitor:
 def __init__(self,path:str|Path):self.path=Path(path)
 def check(self,previous:str|None=None):
  if not self.path.exists():return {'status':'NO_ARCHIVE','changed':False}
  digest=hashlib.sha256(self.path.read_bytes()).hexdigest();return {'status':'OBSERVED','changed':previous is not None and digest!=previous,'sha256':digest}
