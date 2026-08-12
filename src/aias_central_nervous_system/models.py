"""Immutable event envelope and delivery result contracts for AIAS CNS."""
from __future__ import annotations
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import json,uuid
@dataclass(frozen=True,slots=True)
class Event:
 """Versioned immutable message carrying source, correlation and JSON payload."""
 event_id:str;event_type:str;source:str;occurred_at:str;correlation_id:str;schema_version:str;payload:dict
 @classmethod
 def create(cls,event_type:str,source:str,payload:dict,correlation_id:str|None=None)->"Event":
  """Create a globally unique UTC event with a stable schema version."""
  return cls(f"EVT-{uuid.uuid4().hex.upper()}",event_type,source,datetime.now(timezone.utc).isoformat(),correlation_id or f"COR-{uuid.uuid4().hex.upper()}","1.0.0",dict(payload))
 def to_dict(self)->dict:
  """Serialize the immutable event envelope into its journal representation."""
  return asdict(self)
 def validate(self,max_payload_bytes:int=1000000)->None:
  """Reject incomplete identity fields, invalid event types and excessive payloads."""
  if not self.event_id.startswith("EVT-") or "." not in self.event_type or not self.source or not self.correlation_id:raise ValueError("invalid_event_envelope")
  if len(json.dumps(self.payload,ensure_ascii=False).encode())>max_payload_bytes:raise ValueError("payload_too_large")
