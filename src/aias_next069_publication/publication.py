from pathlib import Path
class ArchivePublication:
 def __init__(self,path:str|Path):self.path=Path(path)
 def publish(self):return {'status':'REFERENCE_ARCHIVE' if self.path.exists() else 'NO_ARCHIVE','approval':False}
