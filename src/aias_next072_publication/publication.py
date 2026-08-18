from pathlib import Path
import hashlib
class HistoricalPublication:
 def __init__(self,path:str|Path):self.path=Path(path)
 def publish(self):
  if not self.path.exists():return {'status':'NO_ARCHIVE','approval':False}
  return {'status':'REFERENCE_PUBLICATION','sha256':hashlib.sha256(self.path.read_bytes()).hexdigest(),'approval':False}
