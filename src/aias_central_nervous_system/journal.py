"""Atomic append-oriented event journal with global sequence and consumer cursors."""
from __future__ import annotations
import json,os,tempfile
from pathlib import Path
from .models import Event
class EventJournal:
 """Persist unique events, cursor acknowledgements and dead-letter evidence."""
 def __init__(self,path:Path):self.path=path;self.data=self._load()
 def _load(self):
  if not self.path.exists():return {"schema_version":"1.0.0","events":[],"event_ids":[],"cursors":{},"dead_letters":[]}
  return json.loads(self.path.read_text(encoding="utf-8"))
 def append(self,event:Event)->dict:
  """Append a validated event once and assign its monotonic global sequence."""
  event.validate()
  if event.event_id in self.data["event_ids"]:return next(x for x in self.data["events"] if x["event_id"]==event.event_id)
  row={"sequence":len(self.data["events"])+1,**event.to_dict()};self.data["events"].append(row);self.data["event_ids"].append(event.event_id);self._save();return row
 def pending(self,consumer_id:str,event_types:set[str]|None=None)->list[dict]:
  """Return ordered events after a consumer cursor, optionally filtered by type."""
  cursor=self.data["cursors"].get(consumer_id,0);return [x for x in self.data["events"] if x["sequence"]>cursor and (not event_types or x["event_type"] in event_types)]
 def acknowledge(self,consumer_id:str,sequence:int)->None:
  """Advance a consumer cursor monotonically without allowing skipped journal bounds."""
  current=self.data["cursors"].get(consumer_id,0)
  if sequence<current or sequence>len(self.data["events"]):raise ValueError("invalid_cursor")
  self.data["cursors"][consumer_id]=sequence;self._save()
 def dead_letter(self,consumer_id:str,event:dict,error:str)->None:
  """Persist failed delivery evidence for controlled replay and diagnosis."""
  self.data["dead_letters"].append({"consumer_id":consumer_id,"event_id":event["event_id"],"sequence":event["sequence"],"error":error});self._save()
 def _save(self):
  self.path.parent.mkdir(parents=True,exist_ok=True);fd,name=tempfile.mkstemp(dir=self.path.parent,suffix=".tmp")
  try:
   with os.fdopen(fd,"w",encoding="utf-8") as stream:json.dump(self.data,stream,ensure_ascii=False,indent=2);stream.write("\n")
   os.replace(name,self.path)
  finally:
   if os.path.exists(name):os.unlink(name)
