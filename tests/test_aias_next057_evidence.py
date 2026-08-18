from aias_next057_evidence import ComplianceEvidenceReport
def test_report_has_external_status(tmp_path):assert ComplianceEvidenceReport(tmp_path).build()['external_gates']=='PENDING'
