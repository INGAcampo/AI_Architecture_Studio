from pathlib import Path
import json
class ArchiveVerifier:
 def __init__(self,path:str|Path):self.path=Path(path)
 def run(self):
  if not self.path.exists():return {'status':'NO_ARCHIVE','records':0}
  bad=0;n=0
  for x in self.path.read_text(encoding='utf-8').splitlines():
   if not x.strip():continue
   n+=1
   try:
    if not json.loads(x).get('recorded_at'):bad+=1
   except json.JSONDecodeError:bad+=1
  return {'status':'VALID' if bad==0 else 'INVALID','records':n,'invalid':bad}
