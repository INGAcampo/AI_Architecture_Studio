from aias_next058_closure import RoadmapAuditClosure
def test_closure_holds_missing(tmp_path):assert RoadmapAuditClosure(tmp_path).run()['status']=='HOLD'
