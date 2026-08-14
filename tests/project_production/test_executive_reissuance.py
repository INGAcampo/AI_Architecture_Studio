from aias_executive_reissuance import ExecutiveReissuanceCampaign
def test_backend_fail_closed_and_manifest():
 c=ExecutiveReissuanceCampaign(); assert c.backend_discovery([])['status']=='BLOCKED_BACKEND_UNAVAILABLE'; assert c.manifest([{'status':'BLOCKED'}])['verdict']=='NOT_READY'
def test_xlsx_refresh_tracks_fingerprint():
 assert ExecutiveReissuanceCampaign().xlsx_refresh('new','old')['status']=='REFRESHED'
