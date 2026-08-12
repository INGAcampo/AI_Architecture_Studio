from aias_next051_review import StrategicEvidenceReview
def test_review_missing(tmp_path): assert StrategicEvidenceReview(tmp_path/'x').run()['valid'] is False
