from aias_next038_continuity import ContinuityPublisher
def test_publication_is_not_release_approved(tmp_path):
    p=ContinuityPublisher(tmp_path).publish(); assert p.production_approval=='NOT_GRANTED'
