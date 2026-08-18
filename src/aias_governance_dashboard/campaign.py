from __future__ import annotations
from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True, slots=True)
class CampaignSnapshot:
    observation_days: int
    production_projects: int
    independent_audits: int
    status: str
@dataclass(slots=True)
class CampaignTracker:
    started_on: date | None = None
    observation_days: int = 0
    production_projects: int = 0
    independent_audits: int = 0
    def snapshot(self) -> CampaignSnapshot:
        status="ACTIVE_EVIDENCE_COLLECTION"
        if self.observation_days >= 365 and self.production_projects >= 10 and self.independent_audits >= 1: status="ELIGIBLE_FOR_INDEPENDENT_MATURITY_ASSESSMENT"
        return CampaignSnapshot(self.observation_days,self.production_projects,self.independent_audits,status)
    def record_observation(self, days: int, projects: int = 0) -> CampaignSnapshot:
        if days < 0 or projects < 0: raise ValueError("campaign_counts_cannot_decrease")
        self.observation_days += days; self.production_projects += projects; return self.snapshot()
