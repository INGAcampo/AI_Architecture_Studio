from aias_next044_summary import EvidenceSummary
def test_summary_is_conservative(tmp_path): assert EvidenceSummary(tmp_path).build()['production_release'] is False
