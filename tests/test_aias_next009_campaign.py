import pytest
from aias_governance_dashboard import CampaignTracker
def test_campaign_starts_without_fabricated_evidence():
    snapshot=CampaignTracker().snapshot()
    assert snapshot.observation_days == 0 and snapshot.production_projects == 0 and snapshot.independent_audits == 0
    assert snapshot.status == "ACTIVE_EVIDENCE_COLLECTION"
def test_campaign_requires_all_thresholds():
    tracker=CampaignTracker(); tracker.record_observation(365,10)
    assert tracker.snapshot().status == "ACTIVE_EVIDENCE_COLLECTION"
    tracker.independent_audits=1
    assert tracker.snapshot().status == "ELIGIBLE_FOR_INDEPENDENT_MATURITY_ASSESSMENT"
def test_negative_campaign_counts_rejected():
    with pytest.raises(ValueError): CampaignTracker().record_observation(-1)
