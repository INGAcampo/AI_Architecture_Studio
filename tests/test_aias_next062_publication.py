from aias_next062_publication import RoadmapPublication
def test_publication_holds_missing(tmp_path):assert RoadmapPublication(tmp_path/'x').publish()['status']=='HOLD'
