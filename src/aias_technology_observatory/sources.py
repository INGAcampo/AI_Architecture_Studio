"""Attributable and integrity-protected technology observations."""
from __future__ import annotations
import hashlib
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class Observation:
    """A dated observation derived from an authoritative source."""
    observation_id:str; title:str; source_url:str; publisher:str; observed_on:str; summary:str; domain:str; evidence_strength:float
    @property
    def sha256(self)->str:
        """Hash canonical observation fields for provenance and change detection."""
        return hashlib.sha256(f"{self.title}|{self.source_url}|{self.observed_on}|{self.summary}".encode()).hexdigest()
    def to_dict(self):
        """Serialize the observation together with its provenance digest."""
        return {**asdict(self),"sha256":self.sha256}

def authoritative(observation:Observation)->bool:
    """Check minimum attribution, HTTPS and evidence-strength requirements."""
    return observation.source_url.startswith("https://") and bool(observation.publisher.strip()) and 0<=observation.evidence_strength<=1
