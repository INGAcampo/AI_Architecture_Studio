"""Source, feed-item and observation-cycle contracts for continuous ATO operation."""
from __future__ import annotations
from dataclasses import dataclass,asdict
import hashlib,json
@dataclass(frozen=True,slots=True)
class FeedItem:
 """Attributable external observation with normalized opportunity dimensions."""
 source_id:str; title:str; url:str; published_at:str; summary:str; domain:str
 relevance:float; impact:float; reuse:float; acceleration:float; risk:float
 def fingerprint(self)->str:
  """Hash stable identifying content for cross-cycle deduplication."""
  return hashlib.sha256(f"{self.source_id}|{self.url}|{self.title}".encode()).hexdigest()
 def to_dict(self)->dict:
  """Serialize the feed item and append its deterministic fingerprint."""
  return {**asdict(self),"fingerprint":self.fingerprint()}
