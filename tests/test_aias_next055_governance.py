from aias_next055_governance import RoadmapGovernance
def test_governance_holds_missing(tmp_path):assert RoadmapGovernance(tmp_path/'x').inspect()['status']=='HOLD'
