"""Validation and lookup for explicitly authorized authoritative sources."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse
class SourceRegistry:
 """Enforce HTTPS, host allowlisting, cadence and evidence metadata."""
 def __init__(self,path:Path):self.data=json.loads(path.read_text(encoding="utf-8"));self.sources={x["id"]:x for x in self.data["sources"]};self.validate()
 def validate(self)->None:
  """Reject duplicate identities, insecure URLs and invalid cadence or evidence scores."""
  if len(self.sources)!=len(self.data["sources"]):raise ValueError("duplicate_source")
  for source in self.sources.values():
   parsed=urlparse(source["base_url"])
   if parsed.scheme!="https" or not parsed.hostname:raise ValueError("insecure_source")
   if source["cadence_hours"]<=0 or not 0<=source["evidence_strength"]<=1:raise ValueError("invalid_source_metadata")
 def authorize(self,source_id:str,url:str)->dict:
  """Return source metadata only when an item URL matches its HTTPS host allowlist."""
  source=self.sources.get(source_id)
  if not source:raise ValueError("unknown_source")
  expected=urlparse(source["base_url"]).hostname;actual=urlparse(url).hostname
  if urlparse(url).scheme!="https" or actual!=expected:raise ValueError("source_host_not_allowed")
  return source
