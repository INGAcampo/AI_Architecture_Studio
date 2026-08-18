from aias_next072_publication import HistoricalPublication
def test_missing(tmp_path):assert HistoricalPublication(tmp_path/'x').publish()['approval'] is False
