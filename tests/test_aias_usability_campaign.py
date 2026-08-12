from pathlib import Path

from aias_usability_campaign import SessionRecord, UsabilityCampaign


def test_campaign_starts_incomplete_and_accepts_attested_record(tmp_path: Path):
    campaign = UsabilityCampaign(tmp_path)
    assert campaign.status()["campaign_complete"] is False
    digest = campaign.append(SessionRecord("S-001", "facilitator", "P-001", "2026-08-12T10:00:00Z", "2026-08-12T10:30:00Z", ("open dashboard",), ("task completed",), ("artifact.json",), "CONSENT-001"))
    assert len(digest) == 64
    assert campaign.status()["sessions"] == 1
