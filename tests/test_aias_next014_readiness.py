from pathlib import Path

from aias_next014_readiness import CampaignReadiness


def test_readiness_requires_protocol_but_not_fake_records(tmp_path: Path):
    root = tmp_path
    campaign = root / "engineering/aias/usability_campaign"
    campaign.mkdir(parents=True)
    (campaign / "AIAS_W2_07_SPEC.json").write_text("{}", encoding="utf-8")
    (campaign / "SESSION_TEMPLATE.json").write_text("{}", encoding="utf-8")
    report = CampaignReadiness(root).inspect()
    assert report.ready is True
    assert "awaiting first real session" in report.checklist[1]
