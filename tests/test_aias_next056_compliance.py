from aias_next056_compliance import ComplianceCheck
def test_missing_is_reported(tmp_path):assert ComplianceCheck(tmp_path).run()['status']=='NON_COMPLIANT'
