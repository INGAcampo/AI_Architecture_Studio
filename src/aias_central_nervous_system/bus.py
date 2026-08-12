"""Subscription routing, idempotent delivery and projection coordination."""
from __future__ import annotations
from pathlib import Path
from .journal import EventJournal
from .models import Event
class NervousSystemBus:
 """Circulate durable events through explicitly registered trusted handlers."""
 def __init__(self,journal_path:Path):self.journal=EventJournal(journal_path);self.handlers={}
 def subscribe(self,consumer_id:str,event_types:set[str],handler)->None:
  """Register one trusted in-process consumer and its explicit event-type interests."""
  if consumer_id in self.handlers:raise ValueError("duplicate_consumer")
  self.handlers[consumer_id]=(set(event_types),handler)
 def publish(self,event:Event)->dict:
  """Persist an event before delivery so crashes cannot erase accepted messages."""
  return self.journal.append(event)
 def dispatch(self,consumer_id:str)->dict:
  """Deliver pending events in sequence, acknowledge success and dead-letter failures."""
  if consumer_id not in self.handlers:raise KeyError(consumer_id)
  event_types,handler=self.handlers[consumer_id];delivered=failed=0
  for event in self.journal.pending(consumer_id,event_types):
   try:handler(event);self.journal.acknowledge(consumer_id,event["sequence"]);delivered+=1
   except Exception as error:self.journal.dead_letter(consumer_id,event,f"{type(error).__name__}:{error}");failed+=1;break
  return {"consumer_id":consumer_id,"delivered":delivered,"failed":failed,"cursor":self.journal.data["cursors"].get(consumer_id,0)}
